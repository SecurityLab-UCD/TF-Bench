
# task_id
data/repos/libraries/ghc-prim/GHC/Classes.hs--compare

# poly_type
Ad-hoc

# signature
```haskell
compare :: Ord a => a -> a -> Ordering
```   

# code
```haskell
compare x y = if x == y then EQ
                else if x <= y then LT
                else GT
```

# dependencies
## 0
```haskell
(==) :: Eq a => a -> a -> Bool
```
## 1
```haskell
(<=) :: Ord a => a -> a -> Bool
```
## 2
```haskell
data Ordering = LT | EQ | GT
```
