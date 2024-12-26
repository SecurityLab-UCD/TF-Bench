
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Float.hs--sqrt

# poly_type
Ad-hoc

# signature
```haskell
sqrt :: Floating a => a -> a
```   

# code
```haskell
sqrt x =  x ** oneHalf
```

# dependencies
## 0
```haskell
(**) :: Floating a => a -> a -> a
```
## 1
```haskell
oneHalf :: Floating a => a
```
