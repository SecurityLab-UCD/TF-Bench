
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
pred True = False
pred False = error "bad argument"
pred GT = EQ
pred EQ = LT
pred LT = error "bad argument"
pred c = chr (ord c - 1)
pred x = x - 1
```

# dependencies
## 0
```haskell
class Enum a = {Char, Int, Bool, Ordering}
```
## 1
```haskell
chr :: Int -> Char
```
## 2
```haskell
ord :: Char -> Int
```
## 3
```haskell
(-) :: Int -> Int -> Int
```
## 4
```haskell
data Bool = False | True
```
## 5
```haskell
data Ordering = LT | EQ | GT
```