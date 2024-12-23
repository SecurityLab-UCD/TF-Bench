
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Read.hs--readsPrec

# poly_type
Ad-hoc

# signature
```haskell
readsPrec :: Read a => Int -> ReadS a
```   

# code
```haskell
readsPrec = readPrec_to_S readPrec
```

# dependencies
## 0
```haskell
readPrec_to_S :: ReadPrec a -> (Int -> ReadS a)
```
## 1
```haskell
readPrec :: ReadPrec a
```