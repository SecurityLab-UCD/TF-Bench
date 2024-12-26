
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/Foldable.hs--concat

# poly_type
Ad-hoc

# signature
```haskell
concat :: Foldable t => t [a] -> [a]
```   

# code
```haskell
concat xs = build (\c n -> foldr (\x y -> foldr c y x) n xs)
```

# dependencies
## 0
```haskell
build :: ((a -> b -> b) -> b -> b) -> [a]
```
## 1
```haskell
foldr :: Foldable t => (a -> b -> b) -> b -> t a -> b
```