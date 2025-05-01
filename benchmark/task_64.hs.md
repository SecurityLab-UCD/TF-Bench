
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/Foldable.hs--sum

# poly_type
Ad-hoc

# signature
```haskell
sum :: (Foldable t, Num a) => t a -> a
```   

# code
```haskell
sum = getSum #. foldMap' Sum
```

# dependencies
## 0
```haskell
getSum :: Sum a -> a
```
## 1
```haskell
(#.) :: Coercible b c => (b -> c) -> (a -> b) -> (a -> c)
```
## 2
```haskell
foldMap' :: Monoid m => (a -> m) -> t a -> m
```
## 3
```haskell
newtype Sum a = Sum {getSum :: a}
```