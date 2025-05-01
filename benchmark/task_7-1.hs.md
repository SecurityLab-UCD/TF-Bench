
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Enum.hs--pred-Bool

# poly_type
Monomorphic

# signature
```haskell
pred :: Bool -> Bool
```   

# code
```haskell
pred True = False
pred False = error "bad argument"
```

# dependencies
## 0
```haskell
data Bool = False | True
```