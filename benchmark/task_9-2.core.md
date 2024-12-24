
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Enum.hs--fromEnum-Ordering

# poly_type
Monomorphic

# signature
```haskell
fromEnum :: Ordering -> Int
```   

# code
```haskell
fromEnum LT = 0
fromEnum EQ = 1
fromEnum GT = 2
```

# dependencies
## 0
```haskell
data Ordering = LT | EQ | GT
```
