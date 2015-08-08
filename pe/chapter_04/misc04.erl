-module (misc04).
-export ([tuple_to_list/1, timed_apply/3]).

tuple_to_list (T) -> tuple_to_list_aux (T, 1, tuple_size (T) + 1).

tuple_to_list_aux (_, I, I) -> [];
tuple_to_list_aux (Tuple, From, To) -> [element (From, Tuple) | tuple_to_list_aux (Tuple, From + 1, To)].

timed_apply (M, F, Args) ->
	T1 = now (),
	apply (M, F, Args),
	T2 = now (),
	timestamp_diff (T2, T1).

timestamp_diff ({MegaS2, S2, MicroS2}, {MegaS1, S1, MicroS1}) ->
	normalize_timestamp ({MegaS2 - MegaS1, S2 - S1, MicroS2 - MicroS1}).

normalize_timestamp ({MegaS, S, MicroS}) when S < 0 ->
	normalize_timestamp ({MegaS - 1, S + 1000000, MicroS});
normalize_timestamp ({MegaS, S, MicroS}) when MicroS < 0 ->
	normalize_timestamp ({MegaS, S - 1, MicroS + 1000000});
normalize_timestamp (T) -> T.
