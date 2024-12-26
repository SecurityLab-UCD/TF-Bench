
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/Foldable.hs--concatMap

# poly_type
Ad-hoc

# signature
```haskell
concatMap :: Foldable t => (a -> [b]) -> t a -> [b]
```   

# code
```haskell
concatMap f xs = build (\c n -> foldr (\x b -> foldr c b (f x)) n xs)
```

# dependencies
## 0
```haskell
foldr :: Foldable t => (a -> b -> b) -> b -> t a -> b
```
## 1
```haskell
build :: forall a. (forall b. (a -> b -> b) -> b -> b) -> [a]
```
