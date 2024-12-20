
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Enum.hs--fromEnum-Bool

# poly_type
Monomorphic

# signature
```haskell
fromEnum :: Bool -> Int
```   

# code
```haskell
fromEnum False = 0
fromEnum True  = 1
```

# dependencies
## 0
```haskell
data Bool = False | True
```
