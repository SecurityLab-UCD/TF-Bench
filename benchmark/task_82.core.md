
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/Foldable.hs--any

# poly_type
Ad-hoc

# signature
```haskell
any :: Foldable t => (a -> Bool) -> t a -> Bool
```   

# code
```haskell
any p = getAny #. foldMap (Any #. p)
```

# dependencies
## 0
```haskell
foldMap :: Monoid m => (a -> m) -> t a -> m
```
## 1
```haskell
(#.) :: Coercible b c => (b -> c) -> (a -> b) -> (a -> c)
```
## 2
```haskell
getAny :: Any -> Bool
```
## 3
```haskell
Any :: Bool -> Any
```