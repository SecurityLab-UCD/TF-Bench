
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Num.hs--(-)

# poly_type
Ad-hoc

# signature
```haskell
(-) :: Num a => a -> a -> a
```   

# code
```haskell
x - y = x + negate y
```

# dependencies
## 0
```haskell
(+) :: Num a => a -> a -> a
```
## 1
```haskell
negate :: Num a => a -> a
```
