
# task_id
data/repos/ghc/libraries/ghc-prim/GHC/Classes.hs--(<=)

# poly_type
Ad-hoc

# signature
```haskell
(<=) :: Ord a => a -> a -> Bool
```   

# code
```haskell
x <= y = case compare x y of { GT -> False; _ -> True }
```

# dependencies
## 0
```haskell
compare :: Ord a => a -> a -> Ordering
```
## 1
```haskell
data Ordering = LT | EQ | GT
```
