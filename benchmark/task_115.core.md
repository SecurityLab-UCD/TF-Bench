
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Read.hs--readParen

# poly_type
Parametric

# signature
```haskell
readParen :: Bool -> ReadS a -> ReadS a
```   

# code
```haskell
readParen b g   =  if b then mandatory else optional
                   where optional r  = g r ++ mandatory r
                         mandatory r =
                            lex r >>= \("(", s) ->
                            optional s >>= \(x, t) ->
                            lex t >>= \(")", u) ->
                            return (x, u)

```

# dependencies
## 0
```haskell
(++) :: [a] -> [a] -> [a]
```
## 1
```haskell
return :: Monad m => a -> m a
```
## 2
```haskell
lex :: String -> [(String, String)]
```
## 3
```haskell
(>>=) :: Monad m => m a -> (a -> m b) -> m b
```
## 4
```haskell
type ReadS a = String -> [(a, String)]
```