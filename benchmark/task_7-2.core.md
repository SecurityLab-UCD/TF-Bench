
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Enum.hs--pred-Ordering

# poly_type
Monomorphic


# signature
```haskell
pred :: Ordering -> Ordering
```  

# code
```haskell
pred GT = EQ
pred EQ = LT
pred LT = error "bad argument"
```

# dependencies
## 0
```haskell
data Ordering = LT | EQ | GT
```
