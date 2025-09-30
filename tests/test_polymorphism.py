from tfbench.hs_parser import get_polymorphic_type, PolymorphicType, AST


def test_polymorphism():
    types = """
addInt :: Int -> Int -> Int
map :: (a -> b) -> [a] -> [b]
id :: a -> a
elem :: (Eq a) => a -> [a] -> Bool
f1 :: forall a b. a -> b -> a
"""

    ast = AST(types)
    fn_addInt, fn_map, fn_id, fn_elem, fn_f1 = ast.get_functions()

    assert get_polymorphic_type(fn_addInt.type_signature) == PolymorphicType.MONO
    assert get_polymorphic_type(fn_map.type_signature) == PolymorphicType.PARAMETRIC
    assert get_polymorphic_type(fn_id.type_signature) == PolymorphicType.PARAMETRIC
    assert get_polymorphic_type(fn_elem.type_signature) == PolymorphicType.AD_HOC
    assert get_polymorphic_type(fn_f1.type_signature) == PolymorphicType.RANK_N


if __name__ == "__main__":
    test_polymorphism()
