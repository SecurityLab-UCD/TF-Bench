
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Enum.hs--pred

# poly_type
Ad-hoc

# note
modified

# signature
```haskell
pred :: Enum a => a -> a
```  

# code
```haskell
pred = toEnum . (subtract one) . fromEnum
```

# dependencies
## 0
```haskell
toEnum :: Enum a => Int -> a
```
## 1
```haskell
(.) :: (b -> c) -> (a -> b) -> a -> c
```
## 2
```haskell
subtract :: Num a => a -> a -> a
```
## 3
```haskell
fromEnum :: Enum a => a -> Int
```
## 4
```haskell
one :: Int
```