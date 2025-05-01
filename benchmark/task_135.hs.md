
# task_id
data/repos/ghc/libraries/ghc-prim/GHC/Classes.hs--(==)

# poly_type
Ad-hoc

# signature
```haskell
(==) :: Eq a => a -> a -> Bool
```   

# code
```haskell
x == y = not (x /= y)
```

# dependencies
## 0
```haskell
not :: Bool -> Bool
```
## 1
```haskell
(/=) :: Eq a => a -> a -> Bool
```
