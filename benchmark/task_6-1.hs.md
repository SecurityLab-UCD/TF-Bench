
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Enum.hs--succ-Bool

# poly_type
Monomorphic


# signature
```haskell
succ :: Bool -> Bool
```  

# code
```haskell
succ False = True
succ True  = error "bad argument"
```

# dependencies
## 0
```haskell
data Bool = False | True
```