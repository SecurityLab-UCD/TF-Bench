
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/Foldable.hs--all

# poly_type
Ad-hoc

# signature
```haskell
all :: Foldable t => (a -> Bool) -> t a -> Bool
```   

# code
```haskell
all p = getAll #. foldMap (All #. p)
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
getAll :: All -> Bool
```
## 3
```haskell
newtype All = All { getAll :: Bool }
```