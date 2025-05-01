
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/Foldable.hs--foldMap

# poly_type
Ad-hoc

# signature
```haskell
foldMap :: (Foldable t, Monoid m) => (a -> m) -> t a -> m
```   

# code
```haskell
foldMap f = foldr (mappend . f) mempty
```

# dependencies
## 0
```haskell
foldr :: Foldable t => (a -> b -> b) -> b -> t a -> b
```
## 1
```haskell
mappend :: Monoid m => m -> m -> m
```
## 2
```haskell
(.) :: (b -> c) -> (a -> b) -> a -> c
```
## 3
```haskell
mempty :: Monoid m => m
```
