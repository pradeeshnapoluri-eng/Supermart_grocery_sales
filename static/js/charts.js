document.addEventListener("DOMContentLoaded", function() {
    if (typeof Chart === "undefined") {
        document.body.innerHTML = '<div style="padding:40px;color:red;font-size:20px;">ERROR: Chart.js not loaded. Check static/js/chart.umd.min.js</div>';
        return;
    }
    console.log("Chart.js loaded OK");
});

const COLORS = {
    teal        : "#26a69a",
    tealDark    : "#00796b",
    tealLight   : "#80cbc4",
    tealPale    : "#e0f2f1",
    seaGreen    : "#2e8b57",
    seaLight    : "#43a98c",
    gold        : "#d4af37",
    goldDark    : "#b8960c",
    goldLight   : "#f1c40f",
    mint        : "#00e5cc",
    mintDark    : "#00bfa5",
    silver      : "#bdbdbd",
    silverDark  : "#9e9e9e",
    silverLight : "#eeeeee",
    red         : "#e53935"
};

const CAT_COLORS = [
    "#26a69a",
    "#2e8b57",
    "#d4af37",
    "#00bfa5",
    "#43a98c",
    "#80cbc4",
    "#b8960c"
];

const REGION_COLORS = {
    North : "#26a69a",
    South : "#2e8b57",
    East  : "#d4af37",
    West  : "#00bfa5"
};

const TOOLTIP = {
    backgroundColor : "#00796b",
    titleColor      : "#f1c40f",
    bodyColor       : "#e0f2f1",
    padding         : 12,
    cornerRadius    : 8,
    borderColor     : "#00e5cc",
    borderWidth     : 1
};

const TICK_STYLE = {
    font  : { size: 11, family: "Segoe UI" },
    color : "#546e7a"
};

const GRID_STYLE = {
    color     : "#e0f2f1",
    lineWidth : 1
};

const LEGEND_STYLE = {
    position : "top",
    labels   : {
        font    : { size: 12, family: "Segoe UI" },
        padding : 16,
        color   : "#37474f"
    }
};

function formatINR(v) {
    v = parseFloat(v);
    if (isNaN(v)) return "Rs.0";
    if (v >= 1e7) return "Rs." + (v / 1e7).toFixed(2) + " Cr";
    if (v >= 1e5) return "Rs." + (v / 1e5).toFixed(1) + " L";
    if (v >= 1e3) return "Rs." + (v / 1e3).toFixed(1) + "K";
    return "Rs." + v.toFixed(0);
}

function formatDate(dateStr) {
    var d = new Date(dateStr);
    return d.toLocaleDateString("en-IN", { month: "short", year: "2-digit" });
}

var chartInstances = {};

function destroyChart(id) {
    if (chartInstances[id]) {
        chartInstances[id].destroy();
        delete chartInstances[id];
    }
}

function createChart(id, config) {
    destroyChart(id);
    var el = document.getElementById(id);
    if (!el) return;
    chartInstances[id] = new Chart(el.getContext("2d"), config);
}

function showSection(name, btnEl) {
    document.querySelectorAll(".section").forEach(function(s) {
        s.classList.remove("active");
    });
    document.querySelectorAll(".sidebar-btn").forEach(function(b) {
        b.classList.remove("active");
    });
    document.getElementById(name).classList.add("active");
    if (btnEl) btnEl.classList.add("active");

    if (name === "category")    buildCategorySection();
    if (name === "region")      buildRegionSection();
    if (name === "yearly")      buildYearlySection();
    if (name === "monthly")     buildMonthlySection();
    if (name === "cities")      buildCitiesSection();
    if (name === "subcategory") buildSubcategorySection();
    if (name === "discount")    buildDiscountSection();
    if (name === "ml")          buildMLSection();
    if (name === "performance") buildPerformanceSection();
}

/* ───────────────────────────────
   STARTUP — HOME SECTION
─────────────────────────────── */
function fetchAll() {
    fetch("/api/summary")
        .then(function(r) { return r.json(); })
        .then(function(data) { buildKPICards(data); })
        .catch(function(e) { console.error("summary error", e); });

    fetch("/api/sales_over_time")
        .then(function(r) { return r.json(); })
        .then(function(data) { buildTimelineChart(data); })
        .catch(function(e) { console.error("timeline error", e); });

    fetch("/api/category_sales")
        .then(function(r) { return r.json(); })
        .then(function(data) { buildHomeCategoryChart(data); })
        .catch(function(e) { console.error("home category error", e); });

    fetch("/api/region_sales")
        .then(function(r) { return r.json(); })
        .then(function(data) { buildHomeRegionChart(data); })
        .catch(function(e) { console.error("home region error", e); });
}

/* ───────────────────────────────
   KPI CARDS
─────────────────────────────── */
function buildKPICards(data) {
    var container = document.getElementById("kpi-cards");
    if (!container) return;
    container.innerHTML = "";

    var cards = [
        { label: "Total Orders",    value: parseInt(data.total_orders).toLocaleString("en-IN"), sub: "Grocery orders placed",  cls: "teal-top",   sparkle: "hidden" },
        { label: "Total Sales",     value: formatINR(data.total_sales),                          sub: "Revenue generated",      cls: "gold-top",   sparkle: "gold"   },
        { label: "Total Profit",    value: formatINR(data.total_profit),                         sub: "Net profit earned",      cls: "mint-top",   sparkle: ""       },
        { label: "Avg Order Value", value: "Rs." + parseFloat(data.avg_sales).toFixed(0),        sub: "Per order average",      cls: "sea-top",    sparkle: "hidden" },
        { label: "Avg Profit",      value: "Rs." + parseFloat(data.avg_profit).toFixed(0),       sub: "Per order profit",       cls: "gold-top",   sparkle: "gold"   },
        { label: "Avg Discount",    value: (parseFloat(data.avg_discount) * 100).toFixed(1) + "%", sub: "Average discount given", cls: "silver-top", sparkle: "silver" },
        { label: "Cities Covered",  value: data.total_cities,                                    sub: "Tamil Nadu cities",      cls: "teal-top",   sparkle: "hidden" },
        { label: "Categories",      value: data.total_cats,                                      sub: "Product categories",     cls: "mint-top",   sparkle: ""       }
    ];

    cards.forEach(function(card) {
        var div = document.createElement("div");
        div.className = "kpi-card " + card.cls;
        div.innerHTML =
            '<div class="kpi-sparkle ' + card.sparkle + '"></div>' +
            '<div class="kpi-label">'  + card.label + '</div>'  +
            '<div class="kpi-value">'  + card.value + '</div>'  +
            '<div class="kpi-sub">'    + card.sub   + '</div>';
        container.appendChild(div);
    });
}

/* ───────────────────────────────
   HOME — TIMELINE CHART
─────────────────────────────── */
function buildTimelineChart(data) {
    if (!data.dates || data.dates.length === 0) return;
    createChart("home-timeline-chart", {
        type: "line",
        data: {
            labels: data.dates.map(formatDate),
            datasets: [
                {
                    label           : "Sales",
                    data            : data.sales,
                    borderColor     : COLORS.teal,
                    backgroundColor : COLORS.teal + "22",
                    borderWidth     : 2,
                    pointRadius     : 0,
                    tension         : 0.4,
                    fill            : true
                },
                {
                    label           : "Profit",
                    data            : data.profit,
                    borderColor     : COLORS.gold,
                    backgroundColor : COLORS.gold + "22",
                    borderWidth     : 2,
                    pointRadius     : 0,
                    tension         : 0.4,
                    fill            : true
                }
            ]
        },
        options: {
            responsive          : true,
            maintainAspectRatio : false,
            plugins : { legend: LEGEND_STYLE, tooltip: TOOLTIP },
            scales  : {
                x: { ticks: Object.assign({}, TICK_STYLE, { maxTicksLimit: 12 }), grid: GRID_STYLE },
                y: { ticks: Object.assign({}, TICK_STYLE, { callback: function(v) { return formatINR(v); } }), grid: GRID_STYLE }
            }
        }
    });
}

/* ───────────────────────────────
   HOME — CATEGORY CHART
─────────────────────────────── */
function buildHomeCategoryChart(data) {
    if (!data || data.length === 0) return;
    createChart("home-category-chart", {
        type: "bar",
        data: {
            labels: data.map(function(d) { return d.Category; }),
            datasets: [{
                label           : "Total Sales",
                data            : data.map(function(d) { return d.total_sales; }),
                backgroundColor : CAT_COLORS.map(function(c) { return c + "cc"; }),
                borderColor     : CAT_COLORS,
                borderWidth     : 2,
                borderRadius    : 6
            }]
        },
        options: {
            responsive          : true,
            maintainAspectRatio : false,
            plugins : { legend: { display: false }, tooltip: TOOLTIP },
            scales  : {
                x: { ticks: Object.assign({}, TICK_STYLE, { maxRotation: 30 }), grid: GRID_STYLE },
                y: { ticks: Object.assign({}, TICK_STYLE, { callback: function(v) { return formatINR(v); } }), grid: GRID_STYLE }
            }
        }
    });
}

/* ───────────────────────────────
   HOME — REGION CHART
─────────────────────────────── */
function buildHomeRegionChart(data) {
    if (!data || data.length === 0) return;
    createChart("home-region-chart", {
        type: "doughnut",
        data: {
            labels: data.map(function(d) { return d.Region; }),
            datasets: [{
                data            : data.map(function(d) { return d.total_sales; }),
                backgroundColor : data.map(function(d) { return (REGION_COLORS[d.Region] || COLORS.teal) + "cc"; }),
                borderColor     : data.map(function(d) { return REGION_COLORS[d.Region] || COLORS.teal; }),
                borderWidth     : 2
            }]
        },
        options: {
            responsive          : true,
            maintainAspectRatio : false,
            plugins: {
                legend  : { position: "right", labels: { font: { size: 12 }, padding: 14, color: "#37474f" } },
                tooltip : Object.assign({}, TOOLTIP, { callbacks: { label: function(ctx) { return ctx.label + ": " + formatINR(ctx.parsed); } } })
            }
        }
    });
}

/* ───────────────────────────────
   CATEGORY SECTION
─────────────────────────────── */
var catBuilt = false;
function buildCategorySection() {
    if (catBuilt) return;
    catBuilt = true;
    fetch("/api/category_sales")
        .then(function(r) { return r.json(); })
        .then(function(data) {
            buildCatSalesChart(data);
            buildCatProfitChart(data);
            buildCatOrdersChart(data);
            buildCatAvgChart(data);
            buildCatTable(data);
        })
        .catch(function(e) { console.error("category section error", e); });
}

function buildCatSalesChart(data) {
    createChart("cat-sales-chart", {
        type: "bar",
        data: {
            labels: data.map(function(d) { return d.Category; }),
            datasets: [{
                label: "Total Sales", data: data.map(function(d) { return d.total_sales; }),
                backgroundColor: CAT_COLORS.map(function(c) { return c + "cc"; }),
                borderColor: CAT_COLORS, borderWidth: 2, borderRadius: 6
            }]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { display: false }, tooltip: TOOLTIP },
            scales: {
                x: { ticks: Object.assign({}, TICK_STYLE, { maxRotation: 30 }), grid: GRID_STYLE },
                y: { ticks: Object.assign({}, TICK_STYLE, { callback: function(v) { return formatINR(v); } }), grid: GRID_STYLE }
            }
        }
    });
}

function buildCatProfitChart(data) {
    createChart("cat-profit-chart", {
        type: "bar",
        data: {
            labels: data.map(function(d) { return d.Category; }),
            datasets: [{
                label: "Total Profit", data: data.map(function(d) { return d.total_profit; }),
                backgroundColor: COLORS.seaLight + "cc", borderColor: COLORS.seaGreen,
                borderWidth: 2, borderRadius: 6
            }]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { display: false }, tooltip: TOOLTIP },
            scales: {
                x: { ticks: Object.assign({}, TICK_STYLE, { maxRotation: 30 }), grid: GRID_STYLE },
                y: { ticks: Object.assign({}, TICK_STYLE, { callback: function(v) { return formatINR(v); } }), grid: GRID_STYLE }
            }
        }
    });
}

function buildCatOrdersChart(data) {
    createChart("cat-orders-chart", {
        type: "bar",
        data: {
            labels: data.map(function(d) { return d.Category; }),
            datasets: [{
                label: "Total Orders", data: data.map(function(d) { return d.total_orders; }),
                backgroundColor: COLORS.mint + "cc", borderColor: COLORS.mintDark,
                borderWidth: 2, borderRadius: 6
            }]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { display: false }, tooltip: TOOLTIP },
            scales: {
                x: { ticks: Object.assign({}, TICK_STYLE, { maxRotation: 30 }), grid: GRID_STYLE },
                y: { ticks: TICK_STYLE, grid: GRID_STYLE }
            }
        }
    });
}

function buildCatAvgChart(data) {
    createChart("cat-avg-chart", {
        type: "bar",
        data: {
            labels: data.map(function(d) { return d.Category; }),
            datasets: [{
                label: "Avg Sales", data: data.map(function(d) { return d.avg_sales; }),
                backgroundColor: COLORS.gold + "cc", borderColor: COLORS.goldDark,
                borderWidth: 2, borderRadius: 6
            }]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { display: false }, tooltip: TOOLTIP },
            scales: {
                x: { ticks: Object.assign({}, TICK_STYLE, { maxRotation: 30 }), grid: GRID_STYLE },
                y: { ticks: Object.assign({}, TICK_STYLE, { callback: function(v) { return "Rs." + v.toFixed(0); } }), grid: GRID_STYLE }
            }
        }
    });
}

function buildCatTable(data) {
    var tbody = document.getElementById("cat-table-body");
    if (!tbody) return;
    tbody.innerHTML = "";
    data.forEach(function(row, i) {
        var tr = document.createElement("tr");
        tr.innerHTML =
            '<td><strong style="color:' + CAT_COLORS[i % CAT_COLORS.length] + '">' + row.Category + '</strong></td>' +
            '<td>' + parseInt(row.total_orders).toLocaleString("en-IN") + '</td>' +
            '<td><span class="badge badge-teal">'   + formatINR(row.total_sales)   + '</span></td>' +
            '<td><span class="badge badge-sea">'    + formatINR(row.total_profit)  + '</span></td>' +
            '<td>Rs.' + parseFloat(row.avg_sales).toFixed(0)    + '</td>' +
            '<td>Rs.' + parseFloat(row.avg_profit).toFixed(0)   + '</td>' +
            '<td><span class="badge badge-gold">'  + (parseFloat(row.avg_discount) * 100).toFixed(1) + '%</span></td>';
        tbody.appendChild(tr);
    });
}

/* ───────────────────────────────
   REGION SECTION
─────────────────────────────── */
var regionBuilt = false;
function buildRegionSection() {
    if (regionBuilt) return;
    regionBuilt = true;
    fetch("/api/region_sales")
        .then(function(r) { return r.json(); })
        .then(function(data) {
            buildRegionStatBoxes(data);
            buildRegionSalesChart(data);
            buildRegionProfitChart(data);
        })
        .catch(function(e) { console.error("region section error", e); });
}

function buildRegionStatBoxes(data) {
    var container = document.getElementById("region-stat-boxes");
    if (!container) return;
    container.innerHTML = "";
    data.forEach(function(row) {
        var box = document.createElement("div");
        box.className = "stat-box";
        box.innerHTML =
            '<div class="stat-box-title">' + row.Region + '</div>' +
            '<div class="stat-box-value">' + formatINR(row.total_sales) + '</div>' +
            '<div class="stat-box-label">' + parseInt(row.total_orders).toLocaleString("en-IN") + ' Orders</div>';
        container.appendChild(box);
    });
}

function buildRegionSalesChart(data) {
    createChart("region-sales-chart", {
        type: "bar",
        data: {
            labels: data.map(function(d) { return d.Region; }),
            datasets: [{
                label: "Total Sales", data: data.map(function(d) { return d.total_sales; }),
                backgroundColor: data.map(function(d) { return (REGION_COLORS[d.Region] || COLORS.teal) + "cc"; }),
                borderColor: data.map(function(d) { return REGION_COLORS[d.Region] || COLORS.teal; }),
                borderWidth: 2, borderRadius: 8
            }]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { display: false }, tooltip: TOOLTIP },
            scales: {
                x: { ticks: TICK_STYLE, grid: GRID_STYLE },
                y: { ticks: Object.assign({}, TICK_STYLE, { callback: function(v) { return formatINR(v); } }), grid: GRID_STYLE }
            }
        }
    });
}

function buildRegionProfitChart(data) {
    createChart("region-profit-chart", {
        type: "doughnut",
        data: {
            labels: data.map(function(d) { return d.Region; }),
            datasets: [{
                data: data.map(function(d) { return d.total_profit; }),
                backgroundColor: data.map(function(d) { return (REGION_COLORS[d.Region] || COLORS.teal) + "cc"; }),
                borderColor: data.map(function(d) { return REGION_COLORS[d.Region] || COLORS.teal; }),
                borderWidth: 2
            }]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: {
                legend: { position: "right", labels: { font: { size: 12 }, padding: 14, color: "#37474f" } },
                tooltip: Object.assign({}, TOOLTIP, { callbacks: { label: function(ctx) { return ctx.label + ": " + formatINR(ctx.parsed); } } })
            }
        }
    });
}

/* ───────────────────────────────
   YEARLY SECTION
─────────────────────────────── */
var yearlyBuilt = false;
function buildYearlySection() {
    if (yearlyBuilt) return;
    yearlyBuilt = true;
    fetch("/api/yearly_sales")
        .then(function(r) { return r.json(); })
        .then(function(data) {
            buildYearlyStatBoxes(data);
            buildYearlyChart(data);
            buildYearlyPieChart(data);
        })
        .catch(function(e) { console.error("yearly error", e); });

    fetch("/api/yearly_category")
        .then(function(r) { return r.json(); })
        .then(function(data) { buildYearlyCategoryChart(data); })
        .catch(function(e) { console.error("yearly category error", e); });
}

function buildYearlyStatBoxes(data) {
    var container = document.getElementById("yearly-stat-boxes");
    if (!container) return;
    container.innerHTML = "";
    var colors = [COLORS.teal, COLORS.seaGreen, COLORS.gold, COLORS.mint];
    data.forEach(function(row, i) {
        var box = document.createElement("div");
        box.className = "stat-box";
        box.style.borderTopColor = colors[i % colors.length];
        box.innerHTML =
            '<div class="stat-box-title">' + row.year + '</div>' +
            '<div class="stat-box-value">' + formatINR(row.total_sales) + '</div>' +
            '<div class="stat-box-label">' + parseInt(row.total_orders).toLocaleString("en-IN") + ' Orders</div>';
        container.appendChild(box);
    });
}

function buildYearlyChart(data) {
    createChart("yearly-chart", {
        type: "bar",
        data: {
            labels: data.map(function(d) { return d.year; }),
            datasets: [
                {
                    label: "Sales", data: data.map(function(d) { return d.total_sales; }),
                    backgroundColor: COLORS.teal + "cc", borderColor: COLORS.tealDark,
                    borderWidth: 2, borderRadius: 6
                },
                {
                    label: "Profit", data: data.map(function(d) { return d.total_profit; }),
                    backgroundColor: COLORS.gold + "cc", borderColor: COLORS.goldDark,
                    borderWidth: 2, borderRadius: 6
                }
            ]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: LEGEND_STYLE, tooltip: TOOLTIP },
            scales: {
                x: { ticks: TICK_STYLE, grid: GRID_STYLE },
                y: { ticks: Object.assign({}, TICK_STYLE, { callback: function(v) { return formatINR(v); } }), grid: GRID_STYLE }
            }
        }
    });
}

function buildYearlyPieChart(data) {
    createChart("yearly-pie-chart", {
        type: "pie",
        data: {
            labels: data.map(function(d) { return d.year.toString(); }),
            datasets: [{
                data: data.map(function(d) { return d.total_sales; }),
                backgroundColor: [COLORS.teal + "cc", COLORS.seaGreen + "cc", COLORS.gold + "cc", COLORS.mint + "cc"],
                borderColor: [COLORS.tealDark, COLORS.seaGreen, COLORS.goldDark, COLORS.mintDark],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: {
                legend: { position: "right", labels: { font: { size: 12 }, padding: 12, color: "#37474f" } },
                tooltip: Object.assign({}, TOOLTIP, { callbacks: { label: function(ctx) { return ctx.label + ": " + formatINR(ctx.parsed); } } })
            }
        }
    });
}

function buildYearlyCategoryChart(data) {
    var years = [];
    var cats  = [];
    data.forEach(function(d) {
        if (years.indexOf(d.year) === -1) years.push(d.year);
        if (cats.indexOf(d.Category) === -1) cats.push(d.Category);
    });
    years.sort();

    createChart("yearly-category-chart", {
        type: "bar",
        data: {
            labels: years,
            datasets: cats.map(function(cat, i) {
                return {
                    label: cat,
                    data: years.map(function(y) {
                        var found = data.find(function(d) { return d.year === y && d.Category === cat; });
                        return found ? found.total_sales : 0;
                    }),
                    backgroundColor : CAT_COLORS[i % CAT_COLORS.length] + "cc",
                    borderColor     : CAT_COLORS[i % CAT_COLORS.length],
                    borderWidth     : 1,
                    borderRadius    : 3
                };
            })
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: LEGEND_STYLE, tooltip: TOOLTIP },
            scales: {
                x: { stacked: true, ticks: TICK_STYLE, grid: GRID_STYLE },
                y: { stacked: true, ticks: Object.assign({}, TICK_STYLE, { callback: function(v) { return formatINR(v); } }), grid: GRID_STYLE }
            }
        }
    });
}

/* ───────────────────────────────
   MONTHLY SECTION
─────────────────────────────── */
var monthlyBuilt = false;
function buildMonthlySection() {
    if (monthlyBuilt) return;
    monthlyBuilt = true;
    fetch("/api/monthly_sales")
        .then(function(r) { return r.json(); })
        .then(function(data) {
            buildMonthlySalesChart(data);
            buildMonthlyProfitChart(data);
            buildMonthlyOrdersChart(data);
        })
        .catch(function(e) { console.error("monthly error", e); });
}

function buildMonthlySalesChart(data) {
    createChart("monthly-sales-chart", {
        type: "line",
        data: {
            labels: data.map(function(d) { return d.Month.substring(0, 3); }),
            datasets: [{
                label: "Total Sales", data: data.map(function(d) { return d.total_sales; }),
                borderColor: COLORS.teal, backgroundColor: COLORS.teal + "22",
                borderWidth: 2.5,
                pointRadius: 5, pointBackgroundColor: COLORS.tealDark,
                pointBorderColor: COLORS.mint, pointBorderWidth: 2,
                tension: 0.4, fill: true
            }]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { display: false }, tooltip: TOOLTIP },
            scales: {
                x: { ticks: TICK_STYLE, grid: GRID_STYLE },
                y: { ticks: Object.assign({}, TICK_STYLE, { callback: function(v) { return formatINR(v); } }), grid: GRID_STYLE }
            }
        }
    });
}

function buildMonthlyProfitChart(data) {
    createChart("monthly-profit-chart", {
        type: "bar",
        data: {
            labels: data.map(function(d) { return d.Month.substring(0, 3); }),
            datasets: [{
                label: "Total Profit", data: data.map(function(d) { return d.total_profit; }),
                backgroundColor: COLORS.seaLight + "cc", borderColor: COLORS.seaGreen,
                borderWidth: 2, borderRadius: 4
            }]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { display: false }, tooltip: TOOLTIP },
            scales: {
                x: { ticks: TICK_STYLE, grid: GRID_STYLE },
                y: { ticks: Object.assign({}, TICK_STYLE, { callback: function(v) { return formatINR(v); } }), grid: GRID_STYLE }
            }
        }
    });
}

function buildMonthlyOrdersChart(data) {
    createChart("monthly-orders-chart", {
        type: "bar",
        data: {
            labels: data.map(function(d) { return d.Month.substring(0, 3); }),
            datasets: [{
                label: "Total Orders", data: data.map(function(d) { return d.total_orders; }),
                backgroundColor: COLORS.silver + "cc", borderColor: COLORS.silverDark,
                borderWidth: 2, borderRadius: 4
            }]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { display: false }, tooltip: TOOLTIP },
            scales: {
                x: { ticks: TICK_STYLE, grid: GRID_STYLE },
                y: { ticks: TICK_STYLE, grid: GRID_STYLE }
            }
        }
    });
}

/* ───────────────────────────────
   CITIES SECTION
─────────────────────────────── */
var citiesBuilt = false;
function buildCitiesSection() {
    if (citiesBuilt) return;
    citiesBuilt = true;
    fetch("/api/top_cities")
        .then(function(r) { return r.json(); })
        .then(function(data) {
            buildCitiesSalesChart(data);
            buildCitiesProfitChart(data);
            buildCitiesTable(data);
        })
        .catch(function(e) { console.error("cities error", e); });
}

function buildCitiesSalesChart(data) {
    createChart("cities-sales-chart", {
        type: "bar",
        data: {
            labels: data.map(function(d) { return d.City; }),
            datasets: [{
                label: "Total Sales", data: data.map(function(d) { return d.total_sales; }),
                backgroundColor: COLORS.teal + "cc", borderColor: COLORS.tealDark,
                borderWidth: 2, borderRadius: 4
            }]
        },
        options: {
            indexAxis: "y",
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { display: false }, tooltip: TOOLTIP },
            scales: {
                x: { ticks: Object.assign({}, TICK_STYLE, { callback: function(v) { return formatINR(v); } }), grid: GRID_STYLE },
                y: { ticks: TICK_STYLE, grid: GRID_STYLE }
            }
        }
    });
}

function buildCitiesProfitChart(data) {
    createChart("cities-profit-chart", {
        type: "bar",
        data: {
            labels: data.map(function(d) { return d.City; }),
            datasets: [{
                label: "Total Profit", data: data.map(function(d) { return d.total_profit; }),
                backgroundColor: COLORS.gold + "cc", borderColor: COLORS.goldDark,
                borderWidth: 2, borderRadius: 4
            }]
        },
        options: {
            indexAxis: "y",
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { display: false }, tooltip: TOOLTIP },
            scales: {
                x: { ticks: Object.assign({}, TICK_STYLE, { callback: function(v) { return formatINR(v); } }), grid: GRID_STYLE },
                y: { ticks: TICK_STYLE, grid: GRID_STYLE }
            }
        }
    });
}

function buildCitiesTable(data) {
    var tbody = document.getElementById("cities-table-body");
    if (!tbody) return;
    tbody.innerHTML = "";
    data.forEach(function(row, i) {
        var rankClass = i === 0 ? "rank-1" : i === 1 ? "rank-2" : i === 2 ? "rank-3" : "rank-n";
        var tr = document.createElement("tr");
        tr.innerHTML =
            '<td><span class="rank-badge ' + rankClass + '">' + (i + 1) + '</span></td>' +
            '<td><strong>' + row.City + '</strong></td>' +
            '<td><span class="badge badge-teal">' + formatINR(row.total_sales)  + '</span></td>' +
            '<td><span class="badge badge-sea">'  + formatINR(row.total_profit) + '</span></td>' +
            '<td>' + parseInt(row.total_orders).toLocaleString("en-IN") + '</td>';
        tbody.appendChild(tr);
    });
}

/* ───────────────────────────────
   SUBCATEGORY SECTION
─────────────────────────────── */
var subcatBuilt = false;
function buildSubcategorySection() {
    if (subcatBuilt) return;
    subcatBuilt = true;
    fetch("/api/subcategory_sales")
        .then(function(r) { return r.json(); })
        .then(function(data) {
            buildSubcatSalesChart(data);
            buildSubcatProfitChart(data);
            buildSubcatTable(data);
        })
        .catch(function(e) { console.error("subcategory error", e); });
}

function buildSubcatSalesChart(data) {
    createChart("subcat-sales-chart", {
        type: "bar",
        data: {
            labels: data.map(function(d) { return d["Sub Category"]; }),
            datasets: [{
                label: "Total Sales", data: data.map(function(d) { return d.total_sales; }),
                backgroundColor: COLORS.teal + "cc", borderColor: COLORS.tealDark,
                borderWidth: 2, borderRadius: 4
            }]
        },
        options: {
            indexAxis: "y",
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { display: false }, tooltip: TOOLTIP },
            scales: {
                x: { ticks: Object.assign({}, TICK_STYLE, { callback: function(v) { return formatINR(v); } }), grid: GRID_STYLE },
                y: { ticks: TICK_STYLE, grid: GRID_STYLE }
            }
        }
    });
}

function buildSubcatProfitChart(data) {
    createChart("subcat-profit-chart", {
        type: "bar",
        data: {
            labels: data.map(function(d) { return d["Sub Category"]; }),
            datasets: [{
                label: "Total Profit", data: data.map(function(d) { return d.total_profit; }),
                backgroundColor: COLORS.mint + "cc", borderColor: COLORS.mintDark,
                borderWidth: 2, borderRadius: 4
            }]
        },
        options: {
            indexAxis: "y",
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { display: false }, tooltip: TOOLTIP },
            scales: {
                x: { ticks: Object.assign({}, TICK_STYLE, { callback: function(v) { return formatINR(v); } }), grid: GRID_STYLE },
                y: { ticks: TICK_STYLE, grid: GRID_STYLE }
            }
        }
    });
}

function buildSubcatTable(data) {
    var tbody = document.getElementById("subcat-table-body");
    if (!tbody) return;
    tbody.innerHTML = "";
    data.forEach(function(row) {
        var tr = document.createElement("tr");
        tr.innerHTML =
            '<td><strong>' + row["Sub Category"] + '</strong></td>' +
            '<td><span class="badge badge-teal">' + formatINR(row.total_sales)  + '</span></td>' +
            '<td><span class="badge badge-mint">' + formatINR(row.total_profit) + '</span></td>' +
            '<td>' + parseInt(row.total_orders).toLocaleString("en-IN") + '</td>';
        tbody.appendChild(tr);
    });
}

/* ───────────────────────────────
   DISCOUNT SECTION
─────────────────────────────── */
var discountBuilt = false;
function buildDiscountSection() {
    if (discountBuilt) return;
    discountBuilt = true;
    fetch("/api/discount_analysis")
        .then(function(r) { return r.json(); })
        .then(function(data) {
            buildDiscountChart(data);
            buildMarginChart(data);
        })
        .catch(function(e) { console.error("discount error", e); });

    fetch("/api/profit_rate")
        .then(function(r) { return r.json(); })
        .then(function(data) { buildProfitRateChart(data); })
        .catch(function(e) { console.error("profit rate error", e); });
}

function buildDiscountChart(data) {
    createChart("discount-chart", {
        type: "bar",
        data: {
            labels: data.map(function(d) { return d.Category; }),
            datasets: [{
                label: "Avg Discount %",
                data: data.map(function(d) { return (parseFloat(d.avg_discount) * 100).toFixed(2); }),
                backgroundColor: COLORS.silver + "cc", borderColor: COLORS.silverDark,
                borderWidth: 2, borderRadius: 6
            }]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { display: false }, tooltip: TOOLTIP },
            scales: {
                x: { ticks: Object.assign({}, TICK_STYLE, { maxRotation: 30 }), grid: GRID_STYLE },
                y: { ticks: Object.assign({}, TICK_STYLE, { callback: function(v) { return v + "%"; } }), grid: GRID_STYLE }
            }
        }
    });
}

function buildMarginChart(data) {
    createChart("margin-chart", {
        type: "bar",
        data: {
            labels: data.map(function(d) { return d.Category; }),
            datasets: [{
                label: "Avg Profit Margin %",
                data: data.map(function(d) { return parseFloat(d.avg_profit_margin).toFixed(2); }),
                backgroundColor: COLORS.seaLight + "cc", borderColor: COLORS.seaGreen,
                borderWidth: 2, borderRadius: 6
            }]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { display: false }, tooltip: TOOLTIP },
            scales: {
                x: { ticks: Object.assign({}, TICK_STYLE, { maxRotation: 30 }), grid: GRID_STYLE },
                y: { ticks: Object.assign({}, TICK_STYLE, { callback: function(v) { return v + "%"; } }), grid: GRID_STYLE }
            }
        }
    });
}

function buildProfitRateChart(data) {
    createChart("profit-rate-chart", {
        type: "bar",
        data: {
            labels: data.map(function(d) { return d.category; }),
            datasets: [
                {
                    label: "Profitable Orders",
                    data: data.map(function(d) { return d.profitable_orders; }),
                    backgroundColor: COLORS.teal + "cc", borderColor: COLORS.tealDark,
                    borderWidth: 2, borderRadius: 4
                },
                {
                    label: "Loss Orders",
                    data: data.map(function(d) { return d.loss_orders; }),
                    backgroundColor: COLORS.red + "cc", borderColor: COLORS.red,
                    borderWidth: 2, borderRadius: 4
                }
            ]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: LEGEND_STYLE, tooltip: TOOLTIP },
            scales: {
                x: { ticks: Object.assign({}, TICK_STYLE, { maxRotation: 30 }), grid: GRID_STYLE },
                y: { ticks: TICK_STYLE, grid: GRID_STYLE }
            }
        }
    });
}

/* ───────────────────────────────
   ML SECTION
─────────────────────────────── */
var mlBuilt = false;
function buildMLSection() {
    if (mlBuilt) return;
    mlBuilt = true;
    fetch("/api/ml_results")
        .then(function(r) { return r.json(); })
        .then(function(data) {
            buildMLTable(data);
            buildMLR2Chart(data);
            buildMLRMSEChart(data);
        })
        .catch(function(e) { console.error("ml error", e); });
}

function buildMLTable(data) {
    var tbody = document.getElementById("ml-table-body");
    if (!tbody) return;
    tbody.innerHTML = "";
    var modelColors = ["badge-teal", "badge-sea", "badge-gold"];
    data.forEach(function(row, i) {
        var r2      = parseFloat(row.R2);
        var r2Class = r2 >= 0.9 ? "badge-teal" : r2 >= 0.7 ? "badge-gold" : "badge-red";
        var perf    = r2 >= 0.9 ? "Excellent"  : r2 >= 0.7 ? "Good"       : "Needs Work";
        var tr = document.createElement("tr");
        tr.innerHTML =
            '<td><span class="badge ' + modelColors[i % 3] + '">' + row.Model + '</span></td>' +
            '<td>' + row.RMSE + '</td>' +
            '<td>' + row.MAE  + '</td>' +
            '<td><span class="badge ' + r2Class + '">' + row.R2   + '</span></td>' +
            '<td><span class="badge ' + r2Class + '">' + perf     + '</span></td>';
        tbody.appendChild(tr);
    });
}

function buildMLR2Chart(data) {
    createChart("ml-r2-chart", {
        type: "bar",
        data: {
            labels: data.map(function(d) { return d.Model; }),
            datasets: [{
                label: "R2 Score", data: data.map(function(d) { return d.R2; }),
                backgroundColor: [COLORS.teal + "cc", COLORS.seaGreen + "cc", COLORS.gold + "cc"],
                borderColor: [COLORS.tealDark, COLORS.seaGreen, COLORS.goldDark],
                borderWidth: 2, borderRadius: 6
            }]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { display: false }, tooltip: TOOLTIP },
            scales: {
                x: { ticks: TICK_STYLE, grid: GRID_STYLE },
                y: { min: 0, max: 1, ticks: Object.assign({}, TICK_STYLE, { callback: function(v) { return v.toFixed(2); } }), grid: GRID_STYLE }
            }
        }
    });
}

function buildMLRMSEChart(data) {
    createChart("ml-rmse-chart", {
        type: "bar",
        data: {
            labels: data.map(function(d) { return d.Model; }),
            datasets: [{
                label: "RMSE", data: data.map(function(d) { return d.RMSE; }),
                backgroundColor: [COLORS.silver + "cc", COLORS.mint + "cc", COLORS.gold + "cc"],
                borderColor: [COLORS.silverDark, COLORS.mintDark, COLORS.goldDark],
                borderWidth: 2, borderRadius: 6
            }]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { display: false }, tooltip: TOOLTIP },
            scales: {
                x: { ticks: TICK_STYLE, grid: GRID_STYLE },
                y: { ticks: TICK_STYLE, grid: GRID_STYLE }
            }
        }
    });
}

/* ───────────────────────────────
   PERFORMANCE SECTION
─────────────────────────────── */
var perfBuilt = false;
function buildPerformanceSection() {
    if (perfBuilt) return;
    perfBuilt = true;
    fetch("/api/top_customers")
        .then(function(r) { return r.json(); })
        .then(function(data) { buildCustomersTable(data); })
        .catch(function(e) { console.error("customers error", e); });

    fetch("/api/loss_orders")
        .then(function(r) { return r.json(); })
        .then(function(data) { buildLossTable(data); })
        .catch(function(e) { console.error("loss orders error", e); });
}

function buildCustomersTable(data) {
    var tbody = document.getElementById("customers-table-body");
    if (!tbody) return;
    tbody.innerHTML = "";
    data.forEach(function(row, i) {
        var rankClass = i === 0 ? "rank-1" : i === 1 ? "rank-2" : i === 2 ? "rank-3" : "rank-n";
        var tr = document.createElement("tr");
        tr.innerHTML =
            '<td><span class="rank-badge ' + rankClass + '">' + (i + 1) + '</span></td>' +
            '<td><strong>' + row["Customer Name"] + '</strong></td>' +
            '<td>' + row.total_orders + '</td>' +
            '<td><span class="badge badge-teal">' + formatINR(row.total_sales)                      + '</span></td>' +
            '<td><span class="badge badge-sea">'  + formatINR(row.total_profit)                     + '</span></td>' +
            '<td>Rs.' + parseFloat(row.avg_order_value).toFixed(0) + '</td>';
        tbody.appendChild(tr);
    });
}

function buildLossTable(data) {
    var tbody = document.getElementById("loss-table-body");
    if (!tbody) return;
    tbody.innerHTML = "";
    data.forEach(function(row) {
        var tr = document.createElement("tr");
        tr.innerHTML =
            '<td><span class="badge badge-silver">' + row["Order ID"]       + '</span></td>' +
            '<td>' + row["Customer Name"] + '</td>' +
            '<td><span class="badge badge-teal">'   + row.Category          + '</span></td>' +
            '<td>' + row.City + '</td>' +
            '<td>Rs.' + parseFloat(row.Sales).toFixed(0)  + '</td>' +
            '<td><span class="badge badge-red">Rs.' + parseFloat(row.Profit).toFixed(0) + '</span></td>';
        tbody.appendChild(tr);
    });
}

/* ───────────────────────────────
   INIT
─────────────────────────────── */
fetchAll();