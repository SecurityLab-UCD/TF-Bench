
# task_id
data/repos/ghc/libraries/ghc-prim/GHC/Classes.hs--min

# poly_type
Ad-hoc

# signature
```haskell
min :: Ord a => a -> a -> a
```   

# code
```haskell
min x y = if x <= y then x else y
```

# dependencies
## 0
```haskell
(<=) :: Ord a => a -> a -> Bool
```
