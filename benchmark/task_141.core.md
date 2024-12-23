
# task_id
data/repos/ghc/libraries/ghc-prim/GHC/Classes.hs--(max)

# poly_type
Ad-hoc

# signature
```haskell
max :: Ord a => a -> a -> a
```   

# code
```haskell
max x y = if x <= y then y else x
```

# dependencies
## 0
```haskell
(<=) :: Ord a => a -> a -> Bool
```
