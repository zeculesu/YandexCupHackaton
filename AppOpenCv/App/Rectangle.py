class Rectangle:
    def __init__(self, ctr):
        a, b, c, d = ctr
        vertexes = [a, b, c, d] = a[0], b[0], c[0], d[0]
        self.A = sorted(vertexes, key=lambda t: (t[0], t[1]))[0]
        self.B = sorted(vertexes, key=lambda t: (t[1], -t[0]))[0]
        self.A = sorted(vertexes, key=lambda t: (-t[0], -t[1]))[0]
        self.C = sorted(vertexes, key=lambda t: (-t[1], t[0]))[0]
        
        self.area = int(self.CalculateDistance(self.A, self.B) * self.CalculateDistance(self.B, self.C))
        self.center = (self.A[0] + (self.B[0] - self.A[0]) // 2, self.A[1] + (self.C[1] - self.B[1]) // 2)
         
    def CalculateDistance(self, A, B):
        return ((A[0] - B[0])**2 + (A[1] - B[1])**2)**0.5

