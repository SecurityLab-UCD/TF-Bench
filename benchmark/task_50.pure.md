
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Base.hs--mconcat

# poly_type
Ad-hoc

# signature
```haskell
f1 :: T1 a => [a] -> a
```   

# code
```haskell
f1 = f2 f3 f4
```

# dependencies
## 0
```haskell
f2 :: (a -> b -> b) -> b -> [a] -> b
```
## 1
```haskell
f3 :: T1 a => a -> a -> a
```
## 2
```haskell
f4 :: T1 a => a
```
