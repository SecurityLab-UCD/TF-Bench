
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Num.hs--negate-Int

# poly_type
Monomorphic

# signature
```haskell
negate :: Int -> Int
```   

# code
```haskell
negate x = zero - x
```

# dependencies
## 0
```haskell
(-) :: Num a => a -> a -> a
```
## 1
```haskell
zero :: Int
```
