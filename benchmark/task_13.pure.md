
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Enum.hs--enumFromThenTo

# poly_type
Ad-hoc

# signature
```haskell
f1 :: T1 a => a -> a -> a -> [a]
```   

# code
```haskell
f1 x1 x2 y = f2 f3 [f4 x1, f4 x2 .. f4 y]
```

# dependencies
## 0
```haskell
f2 :: (a -> b) -> [a] -> [b]
```
## 1
```haskell
f3 :: T1 a => T2 -> a
```
## 2
```haskell
f4 :: T1 => a -> T2
```