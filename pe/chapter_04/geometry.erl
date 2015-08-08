-module (geometry).
-export ([area/1, perimeter/1, hypot/2]).

area ({rectangle, Width, Height}) -> Width * Height;
area ({square, Side}) -> Side * Side;
area ({circle, Radius}) -> math:pi () * Radius * Radius;
area ({ra_triangle, Leg1, Leg2}) -> Leg1 * Leg2 / 2.

perimeter ({rectangle, Width, Height}) -> 2 * (Width + Height);
perimeter ({square, Side}) -> 4 * Side;
perimeter ({circle, Radius}) -> 2 * math:pi () * Radius;
perimeter ({ra_triangle, Leg1, Leg2}) -> Leg1 + Leg2 + hypot (Leg1, Leg2).

hypot (X, Y) -> math:sqrt (X * X + Y * Y).
