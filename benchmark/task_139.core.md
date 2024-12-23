
# task_id
data/repos/ghc/libraries/ghc-prim/GHC/Classes.hs--(<)

# poly_type
Ad-hoc

# signature
```haskell
(<) :: Ord a => a -> a -> Bool
```   

# code
```haskell
x < y = not (y <= x>)
```

# dependencies
## 0
```haskell
(<=) :: Ord a => a -> a -> Bool
```
