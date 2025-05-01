
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/Foldable.hs--foldMap-List

# poly_type
Ad-hoc

# signature
```haskell
foldMap :: Monoid m => (a -> m) -> [a] -> m
```   

# code
```haskell
foldMap = (mconcat .) . map
```

# dependencies
## 0
```haskell
mconcat :: Monoid a => [a] -> a
```
## 1
```haskell
(.) :: (b -> c) -> (a -> b) -> a -> c
```
## 2
```haskell
map :: (a -> b) -> [a] -> [b]
```