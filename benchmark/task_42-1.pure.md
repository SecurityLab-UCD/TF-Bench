
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Float.hs--isInfinite-Float

# poly_type
Monomorphic

# signature
```haskell
f1 :: T1 -> T2
```   

# code
```haskell
f1 x = 0 /= f2 x
```

# dependencies
## 0
```haskell
f2 :: T1 -> T3
```
##
```haskell
(/=) :: T3 -> T3 -> T2
```
