
    var StatisticWidgets = function () {

        var _progressIcon = function(element, radius, border, backgroundColor, foregroundColor, end, iconClass) {
        if (typeof d3 == 'undefined') {
            console.warn('Warning - d3.min.js is not loaded.');
            return;
        }

        // Initialize chart only if element exsists in the DOM
        if(element) {


            // Basic setup
            // ------------------------------

            // Main variables
            var d3Container = d3.select(element),
                startPercent = 0,
                iconSize = 32,
                endPercent = end,
                twoPi = Math.PI * 2,
                formatPercent = d3.format('.0%'),
                boxSize = radius * 2;

            // Values count
            var count = Math.abs((endPercent - startPercent) / 0.01);

            // Values step
            var step = endPercent < startPercent ? -0.01 : 0.01;


            // Create chart
            // ------------------------------

            // Add SVG element
            var container = d3Container.append('svg');

            // Add SVG group
            var svg = container
                .attr('width', boxSize)
                .attr('height', boxSize)
                .append('g')
                    .attr('transform', 'translate(' + (boxSize / 2) + ',' + (boxSize / 2) + ')');


            // Construct chart layout
            // ------------------------------

            // Arc
            var arc = d3.svg.arc()
                .startAngle(0)
                .innerRadius(radius)
                .outerRadius(radius - border)
                .cornerRadius(20);


            //
            // Append chart elements
            //

            // Paths
            // ------------------------------

            // Background path
            svg.append('path')
                .attr('class', 'd3-progress-background')
                .attr('d', arc.endAngle(twoPi))
                .style('fill', backgroundColor);

            // Foreground path
            var foreground = svg.append('path')
                .attr('class', 'd3-progress-foreground')
                .attr('filter', 'url(#blur)')
                .style({
                    'fill': foregroundColor,
                    'stroke': foregroundColor
                });

            // Front path
            var front = svg.append('path')
                .attr('class', 'd3-progress-front')
                .style({
                    'fill': foregroundColor,
                    'fill-opacity': 1
                });


            // Text
            // ------------------------------

            // Percentage text value
            var numberText = d3.select('.progress-percentage')
                    .attr('class', 'pt-1 mt-2 mb-1');

            // Icon
            d3.select(element)
                .append("i")
                    .attr("class", iconClass + " counter-icon")
                    .style({
                        'color': foregroundColor,
                        'top': ((boxSize - iconSize) / 2) + 'px'
                    });


            // Animation
            // ------------------------------

            // Animate path
            function updateProgress(progress) {
                foreground.attr('d', arc.endAngle(twoPi * progress));
                front.attr('d', arc.endAngle(twoPi * progress));
                numberText.text(formatPercent(progress));
            }

            // Animate text
            var progress = startPercent;
            (function loops() {
                updateProgress(progress);
                if (count > 0) {
                    count--;
                    progress += step;
                    setTimeout(loops, 10);
                }
            })();
        }
    };


        return {
            init: function () {
               // _areaChartWidget("#chart_area_basic", 50, '#5C6BC0');
               // _areaChartWidget("#chart_area_color", 50, 'rgba(255,255,255,0.75)');

                //_barChartWidget("#chart_bar_basic", 24, 50, true, "elastic", 1200, 50, "#EF5350", "members");
               // _barChartWidget("#chart_bar_color", 24, 50, true, "elastic", 1200, 50, "rgba(255,255,255,0.75)", "members");

               // _lineChartWidget('#line_chart_simple', 50, '#2196F3', 'rgba(33,150,243,0.5)', '#2196F3', '#fff');
               // _lineChartWidget('#line_chart_color', 50, '#fff', 'rgba(255,255,255,0.5)', '#fff', '#29B6F6');

               // _sparklinesWidget("#sparklines_basic", "area", 30, 50, "basis", 750, 2000, "#66BB6A");
                //_sparklinesWidget("#sparklines_color", "area", 30, 50, "basis", 750, 2000, "rgba(255,255,255,0.75)");

                _progressIcon('#progress_icon_one', 42, 2.5, "#eee", "#EF5350", 0.68, "icon-heart6");
                _progressIcon('#progress_icon_two', 42, 2.5, "#eee", "#5C6BC0", 0.82, "icon-trophy3");
                _progressIcon('#progress_icon_three', 42, 2.5, "#00897B", "#fff", 0.73, "icon-bag");
                _progressIcon('#progress_icon_four', 42, 2.5, "#673AB7", "#fff", 0.49, "icon-truck");

                //_progressPercentage('#progress_percentage_one', 46, 3, "#eee", "#2196F3", 0.79);
                //_progressPercentage('#progress_percentage_two', 46, 3, "#eee", "#EF5350", 0.62);
                //_progressPercentage('#progress_percentage_three', 46, 3, "#039BE5", "#fff", 0.69);
               // _progressPercentage('#progress_percentage_four', 46, 3, "#E53935", "#fff", 0.43);

               // _animatedPie("#pie_basic", 120);
               // _animatedPieWithLegend("#pie_basic_legend", 120);
               // _pieArcWithLegend("#pie_arc_legend", 170);
                //_animatedDonut("#donut_basic_stats", 120);
                //_animatedDonutWithLegend("#donut_basic_legend", 120);
               // _donutWithDetails("#donut_basic_details", 146);
               // _progressArcSingle("#arc_single", 78);
               // _progressArcMulti("#arc_multi", 78, 700);
               // _roundedProgressSingle("#rounded_progress_single", 150, 700, '#EC407A');
               // _roundedProgressMultiple("#rounded_progress_multiple", 140);
               // _pieWithProgress("#pie_progress_bar", 146);
               // _segmentedGauge("#segmented_gauge", 200, 0, 100, 5);
            }
        }

    }();

    document.addEventListener('DOMContentLoaded', function () {
        StatisticWidgets.init();
    });
