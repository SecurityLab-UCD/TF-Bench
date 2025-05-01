
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Enum.hs--succ-Int

# poly_type
Monomorphic


# signature
```haskell
succ :: Int -> Int
```  

# code
```haskell
succ x = x + one
```

# dependencies
## 0
```haskell
(+) :: Ord a => a -> a -> a
```
## 1
```haskell
one :: Int
```