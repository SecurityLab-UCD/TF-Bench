
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Enum.hs--toEnum-Ordering

# poly_type
Monomorphic

# signature
```haskell
toEnum :: Int -> Ordering
```   

# code
```haskell
toEnum n | n == 0 = LT
         | n == 1 = EQ
         | n == 2 = GT
         | otherwise = error "bad argument"
```

# dependencies
## 0
```haskell
data Ordering = LT | EQ | GT
```
