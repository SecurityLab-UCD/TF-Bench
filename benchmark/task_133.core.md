
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Base.hs--(&&)

# poly_type
Monomorphic

# signature
```haskell
(&&) :: Bool -> Bool -> Bool
```   

# code
```haskell
(&&) True True = True
(&&) _    _    = False
```

# dependencies
## 0
```haskell
data Bool = True | False
```
