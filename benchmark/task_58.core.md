
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/Foldable.hs--foldr

# poly_type
Ad-hoc

# signature
```haskell
foldr :: Foldable t => (a -> b -> b) -> b -> t a -> b
```   

# code
```haskell
foldr f z t = appEndo (foldMap (Endo #. f) t) z
```

# dependencies
## 0
```haskell
appEndo :: Endo a -> a -> a
```
## 1
```haskell
foldMap :: Monoid m => (a -> m) -> t a -> m
```
## 2
```haskell
(#.) :: Coercible b c => (b -> c) -> (a -> b) -> (a -> c)
```
