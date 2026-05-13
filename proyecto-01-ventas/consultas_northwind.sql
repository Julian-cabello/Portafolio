-- ============================================================
-- ANÁLISIS DE VENTAS — NORTHWIND TRADERS
-- Autor: Julián Cabello | Data Analyst
-- Dataset: Northwind SQLite (jpwhite3)
-- ============================================================


-- ============================================================
-- NIVEL 1 — EXPLORACIÓN BÁSICA
-- Conceptos: SELECT, WHERE, ORDER BY, LIMIT
-- ============================================================

-- 1.1 Ver todos los clientes
SELECT * 
FROM Customers;

-- 1.2 Ver solo columnas relevantes de clientes
SELECT 
    CustomerID,
    CompanyName,
    Country,
    City
FROM Customers;

-- 1.3 Clientes ordenados por país
SELECT 
    CompanyName,
    Country,
    City
FROM Customers
ORDER BY Country ASC, City ASC;

-- 1.4 Clientes de Alemania
SELECT 
    CompanyName,
    City
FROM Customers
WHERE Country = 'Germany';

-- 1.5 Productos con precio mayor a $50
SELECT 
    ProductName,
    UnitPrice
FROM Products
WHERE UnitPrice > 50
ORDER BY UnitPrice DESC;

-- 1.6 Los 10 productos más caros
SELECT 
    ProductName,
    UnitPrice
FROM Products
ORDER BY UnitPrice DESC
LIMIT 10;

-- 1.7 Productos discontinuados
SELECT 
    ProductName,
    UnitPrice
FROM Products
WHERE Discontinued = 1
ORDER BY ProductName;

-- 1.8 Pedidos realizados en 1997
SELECT 
    OrderID,
    CustomerID,
    OrderDate
FROM Orders
WHERE OrderDate BETWEEN '1997-01-01' AND '1997-12-31'
ORDER BY OrderDate;


-- ============================================================
-- NIVEL 2 — AGREGACIONES
-- Conceptos: COUNT, SUM, AVG, MAX, MIN, GROUP BY, HAVING
-- ============================================================

-- 2.1 Total de clientes por país
SELECT 
    Country,
    COUNT(CustomerID) AS total_clientes
FROM Customers
GROUP BY Country
ORDER BY total_clientes DESC;

-- 2.2 Total de productos por categoría
SELECT 
    CategoryID,
    COUNT(ProductID)  AS total_productos,
    ROUND(AVG(UnitPrice), 2) AS precio_promedio,
    MAX(UnitPrice)    AS precio_maximo,
    MIN(UnitPrice)    AS precio_minimo
FROM Products
GROUP BY CategoryID
ORDER BY total_productos DESC;

-- 2.3 Total de pedidos por cliente
SELECT 
    CustomerID,
    COUNT(OrderID) AS total_pedidos
FROM Orders
GROUP BY CustomerID
ORDER BY total_pedidos DESC
LIMIT 10;

-- 2.4 Países con más de 5 clientes
SELECT 
    Country,
    COUNT(CustomerID) AS total_clientes
FROM Customers
GROUP BY Country
HAVING total_clientes > 5
ORDER BY total_clientes DESC;

-- 2.5 Ingresos totales por producto
SELECT 
    ProductID,
    ROUND(SUM(Quantity * UnitPrice), 2) AS ingresos_totales,
    SUM(Quantity)                        AS unidades_vendidas
FROM [Order Details]
GROUP BY ProductID
ORDER BY ingresos_totales DESC
LIMIT 10;


-- ============================================================
-- NIVEL 3 — JOINS
-- Conceptos: INNER JOIN, LEFT JOIN, múltiples tablas
-- ============================================================

-- 3.1 Productos con nombre de categoría (INNER JOIN)
SELECT 
    p.ProductName,
    c.CategoryName,
    p.UnitPrice,
    p.UnitsInStock
FROM Products p
INNER JOIN Categories c ON p.CategoryID = c.CategoryID
ORDER BY c.CategoryName, p.ProductName;

-- 3.2 Pedidos con nombre del cliente
SELECT 
    o.OrderID,
    c.CompanyName,
    c.Country,
    o.OrderDate
FROM Orders o
INNER JOIN Customers c ON o.CustomerID = c.CustomerID
ORDER BY o.OrderDate DESC
LIMIT 20;

-- 3.3 Detalle completo de ventas — JOIN de 4 tablas
SELECT 
    o.OrderID,
    o.OrderDate,
    c.CompanyName         AS cliente,
    c.Country,
    p.ProductName         AS producto,
    cat.CategoryName      AS categoria,
    od.Quantity           AS cantidad,
    od.UnitPrice          AS precio_unitario,
    ROUND(od.Quantity * od.UnitPrice, 2) AS total_linea
FROM Orders o
INNER JOIN Customers c        ON o.CustomerID  = c.CustomerID
INNER JOIN [Order Details] od ON o.OrderID     = od.OrderID
INNER JOIN Products p         ON od.ProductID  = p.ProductID
INNER JOIN Categories cat     ON p.CategoryID  = cat.CategoryID
ORDER BY o.OrderDate DESC;

-- 3.4 Ventas totales por categoría con JOIN
SELECT 
    cat.CategoryName,
    COUNT(DISTINCT o.OrderID)            AS total_pedidos,
    SUM(od.Quantity)                     AS unidades_vendidas,
    ROUND(SUM(od.Quantity * od.UnitPrice), 2) AS ingresos_totales
FROM Categories cat
INNER JOIN Products p         ON cat.CategoryID = p.CategoryID
INNER JOIN [Order Details] od ON p.ProductID    = od.ProductID
INNER JOIN Orders o           ON od.OrderID     = o.OrderID
GROUP BY cat.CategoryName
ORDER BY ingresos_totales DESC;

-- 3.5 Empleados con sus ventas totales
SELECT 
    e.FirstName || ' ' || e.LastName AS empleado,
    e.Title                          AS cargo,
    COUNT(DISTINCT o.OrderID)        AS pedidos_gestionados,
    ROUND(SUM(od.Quantity * od.UnitPrice), 2) AS ventas_totales
FROM Employees e
INNER JOIN Orders o           ON e.EmployeeID = o.EmployeeID
INNER JOIN [Order Details] od ON o.OrderID    = od.OrderID
GROUP BY e.EmployeeID
ORDER BY ventas_totales DESC;

-- 3.6 Clientes sin pedidos (LEFT JOIN)
SELECT 
    c.CompanyName,
    c.Country,
    o.OrderID
FROM Customers c
LEFT JOIN Orders o ON c.CustomerID = o.CustomerID
WHERE o.OrderID IS NULL;


-- ============================================================
-- NIVEL 4 — SUBCONSULTAS Y ANÁLISIS AVANZADO
-- Conceptos: Subqueries, CTEs, CASE, ROUND, DATE
-- ============================================================

-- 4.1 Productos con precio mayor al promedio general
SELECT 
    ProductName,
    UnitPrice,
    ROUND(UnitPrice - (SELECT AVG(UnitPrice) FROM Products), 2) AS diferencia_vs_promedio
FROM Products
WHERE UnitPrice > (SELECT AVG(UnitPrice) FROM Products)
ORDER BY UnitPrice DESC;

-- 4.2 Top 5 clientes por ingresos generados
SELECT 
    c.CompanyName,
    c.Country,
    ROUND(SUM(od.Quantity * od.UnitPrice), 2) AS ingresos_generados
FROM Customers c
INNER JOIN Orders o           ON c.CustomerID = o.CustomerID
INNER JOIN [Order Details] od ON o.OrderID    = od.OrderID
GROUP BY c.CustomerID
ORDER BY ingresos_generados DESC
LIMIT 5;

-- 4.3 Ventas mensuales — tendencia en el tiempo
SELECT 
    STRFTIME('%Y-%m', o.OrderDate) AS mes,
    COUNT(DISTINCT o.OrderID)       AS total_pedidos,
    ROUND(SUM(od.Quantity * od.UnitPrice), 2) AS ingresos_mes
FROM Orders o
INNER JOIN [Order Details] od ON o.OrderID = od.OrderID
GROUP BY mes
ORDER BY mes;

-- 4.4 Clasificación de clientes por volumen de compra (CASE)
SELECT 
    c.CompanyName,
    c.Country,
    ROUND(SUM(od.Quantity * od.UnitPrice), 2) AS total_comprado,
    CASE 
        WHEN SUM(od.Quantity * od.UnitPrice) >= 50000 THEN 'Premium'
        WHEN SUM(od.Quantity * od.UnitPrice) >= 20000 THEN 'Regular'
        ELSE 'Ocasional'
    END AS segmento
FROM Customers c
INNER JOIN Orders o           ON c.CustomerID = o.CustomerID
INNER JOIN [Order Details] od ON o.OrderID    = od.OrderID
GROUP BY c.CustomerID
ORDER BY total_comprado DESC;

-- 4.5 CTE — Análisis de rentabilidad por categoría
WITH ventas_categoria AS (
    SELECT 
        cat.CategoryName,
        ROUND(SUM(od.Quantity * od.UnitPrice), 2) AS ingresos
    FROM Categories cat
    INNER JOIN Products p         ON cat.CategoryID = p.CategoryID
    INNER JOIN [Order Details] od ON p.ProductID    = od.ProductID
    GROUP BY cat.CategoryName
),
total AS (
    SELECT SUM(ingresos) AS gran_total FROM ventas_categoria
)
SELECT 
    vc.CategoryName,
    vc.ingresos,
    ROUND(vc.ingresos * 100.0 / t.gran_total, 2) AS porcentaje_participacion
FROM ventas_categoria vc, total t
ORDER BY vc.ingresos DESC;

-- 4.6 Productos con stock crítico vs ventas recientes
SELECT 
    p.ProductName,
    p.UnitsInStock                               AS stock_actual,
    p.ReorderLevel                               AS nivel_reorden,
    COALESCE(SUM(od.Quantity), 0)               AS unidades_vendidas,
    CASE 
        WHEN p.UnitsInStock <= p.ReorderLevel THEN '⚠ Reabastecer'
        ELSE '✓ OK'
    END AS estado_stock
FROM Products p
LEFT JOIN [Order Details] od ON p.ProductID = od.ProductID
GROUP BY p.ProductID
ORDER BY stock_actual ASC
LIMIT 15;

-- 4.7 Ranking de productos por categoría usando subconsulta
SELECT 
    cat.CategoryName,
    p.ProductName,
    ROUND(SUM(od.Quantity * od.UnitPrice), 2) AS ingresos,
    (
        SELECT COUNT(*) 
        FROM Products p2
        INNER JOIN [Order Details] od2 ON p2.ProductID = od2.ProductID
        WHERE p2.CategoryID = p.CategoryID
        AND SUM(od2.Quantity * od2.UnitPrice) >= SUM(od.Quantity * od.UnitPrice)
    ) AS ranking_en_categoria
FROM Products p
INNER JOIN Categories cat     ON p.CategoryID  = cat.CategoryID
INNER JOIN [Order Details] od ON p.ProductID   = od.ProductID
GROUP BY p.ProductID
ORDER BY cat.CategoryName, ingresos DESC;