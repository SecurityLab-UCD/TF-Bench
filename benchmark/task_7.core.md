
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
pred (c :: Char) =  chr (ord c - 1)
pred True = False
pred (x :: Int) = x - 1
```

# dependencies
## 0
```haskell
class Enum a = {Char, Int, Bool}
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