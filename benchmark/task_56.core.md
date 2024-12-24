
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/Foldable.hs--elem

# poly_type
Ad-hoc

# signature
```haskell
elem :: (Foldable t, Eq a) => a -> t a -> Bool
```   

# code
```haskell
elem = any . (==)
```

# dependencies
## 0
```haskell
any :: Foldable t => (a -> Bool) -> t a -> Bool
```
## 1
```haskell
(.) :: (b -> c) -> (a -> b) -> a -> c
```
## 2
```haskell
(==) :: Eq a => a -> a -> Bool
```