from __future__ import annotations
from otex.primitives.liquidity_pool import AbstractLiquidityPoolPrimitive
from otex.utils.https_utils import Call, Response
from otex.utils.memory_utils import StatesBuffer 
from sample_integration.uniswap.uniswap_v2.uniswap_v2_helper import UniswapV2HelperHook
from typing import List


UniswapV2HelperHook = UniswapV2HelperHook()

class UniswapV2PoolHook(AbstractLiquidityPoolPrimitive):
    
	def __init__(
		self,
		pool_record: dict
	) -> None:
		self.chain_id = pool_record["chain_id"]
		self.protocol_id = pool_record["protocol_id"]
		self.pool_address = pool_record["pool_address"]
		self.tokens = pool_record["tokens"]
		self.computation_units = pool_record["computation_units"]
		self.protocol_utils = pool_record["protocol_utils"]
		
		if "states" in pool_record:
			self.states = StatesBuffer(states_record = pool_record["states"])
		else:
			self.states = StatesBuffer()
	
	def to_dict(
		self,
		deep = False
	) -> dict:
		
		p = dict()
		p["chain_id"] = self.chain_id
		p["protocol_id"] = self.protocol_id
		p["pool_address"] = self.pool_address
		p["tokens"] = self.tokens
		p["computation_units"] = self.computation_units
		p["protocol_utils"] = self.protocol_utils
		
		if deep:
			p["states"] = self.states.to_dict()
		return p
	
	def get_states_calls(
		self
	) -> list[Call]:
		queries = list()
		call = UniswapV2HelperHook.get_reserves_call(pool_address = self.pool_address)
		queries.append(call)
		return queries
	
	def get_dependent_states_calls(
		self
	) -> List[Call]:
		pass

	def process_pool_state_call_response(
		self,
		data: Response
	):
		if data.attribute == 'balances':
			state =  UniswapV2HelperHook.process_reserves_call(
											data = data
										)
			self.states.add_state(name = "reserve0", value = state[0])
			self.states.add_state(name = "reserve1", value = state[1])
		else:
			raise Exception("### ERROR: Uknown attribute for Uniswap v2")
	
		
	def has_complete_pool_states(
		self
	) -> bool:

		complete = True
		if not hasattr(self.states, 'reserve0'):
			complete = False
		if not hasattr(self.states, 'reserve1'):
			complete = False
		return complete
	
	def get_amount_out(
		self,
		token_in:str,
		amount_in:int
	) -> tuple[int | None, int | None]:
		'''
			Calculation for amount out of constant-product pools given reserves.

			Source sample:
			https://etherscan.io/address/0x7a250d5630b4cf539739df2c5dacb4c659f2488d#code 
		'''
		
		if token_in == self.protocol_utils["token0"]:
			reserve_in = self.states.reserve0
			reserve_out = self.states.reserve1
		else:
			reserve_in = self.states.reserve1
			reserve_out = self.states.reserve0
		if not (reserve_in > 0 and reserve_out > 0):
			return 0, 0
		amount_in_with_fee = amount_in * 997
		fee_amount = int(amount_in * 0.003)
		numerator = amount_in_with_fee * reserve_out
		denominator = reserve_in * 1000 + amount_in_with_fee
		amount_out = int(numerator/denominator)
		return fee_amount, amount_out

	def get_amount_in(
		self,
		token_out:str,
		amount_out:int
	) -> tuple[int | None, int | None]:
		'''
			Calculation for amount out of constant-product pools given reserves.

			Source sample:
			https://etherscan.io/address/0x7a250d5630b4cf539739df2c5dacb4c659f2488d#code 
		'''
		if token_out == self.protocol_utils["token0"]:
			reserve_in = self.states.reserve0
			reserve_out = self.states.reserve1
		else:
			reserve_in = self.states.reserve1
			reserve_out = self.states.reserve0

		if not (reserve_in > 0 and reserve_out > 0):
			return 0, 0
		amount_out = int(amount_out)
		numerator = reserve_in * amount_out * 1000
		denominator = (reserve_out - amount_out) * 997
		amount_in =  (numerator / denominator) + 1
		if amount_in < 0:
			return None, None
		fee_amount = int(amount_in * 0.003)
		return fee_amount, amount_in

	def get_interaction_encoding_utils(
		self,
		token_in:str,
		amount_in:int, 
		token_out:str, 
		amount_out:int
	) -> dict:
		
		encoding_utils = dict()
		encoding_utils["path"] = [token_in, token_out]
		return encoding_utils