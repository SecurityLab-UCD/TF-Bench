
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Enum.hs--pred-Int

# poly_type
Monomorphic


# signature
```haskell
pred :: Int -> Int
```  

# code
```haskell
pred x = x - one
```

# dependencies
## 0
```haskell
(-) :: Num a => a -> a -> a
```
## 1
```haskell
one :: Int
```