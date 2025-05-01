
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Enum.hs--succ-Ordering

# poly_type
Monomorphic


# signature
```haskell
succ :: Ordering -> Ordering
```  

# code
```haskell
succ LT = EQ
succ EQ = GT
succ GT = error "bad argument"
```

# dependencies
## 0
```haskell
data Ordering = LT | EQ | GT
```
