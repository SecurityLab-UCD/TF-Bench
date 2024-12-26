
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Enum.hs--succ

# poly_type
Ad-hoc

# note
modified

# signature
```haskell
succ :: Enum a => a -> a
```  

# code
```haskell
succ = toEnum . (+ one) . fromEnum
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
(+) :: Num a => a -> a -> a
```
## 3
```haskell
fromEnum :: Enum a => a -> Int
```
## 4
```haskell
one :: Int
```