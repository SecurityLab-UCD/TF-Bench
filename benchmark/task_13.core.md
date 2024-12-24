
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Enum.hs--enumFromThenTo

# poly_type
Ad-hoc

# signature
```haskell
enumFromThenTo :: Enum a => a -> a -> a -> [a]
```   

# code
```haskell
enumFromThenTo x1 x2 y = map toEnum [fromEnum x1, fromEnum x2 .. fromEnum y]
```

# dependencies
## 0
```haskell
map :: (a -> b) -> [a] -> [b]
```
## 1
```haskell
toEnum :: Enum a => Int -> a
```
## 2
```haskell
fromEnum :: Enum => a -> Int
```