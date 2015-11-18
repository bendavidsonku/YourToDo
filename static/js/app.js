$(document).ready(function() {
    // Navigation bar profile hover effect
    $('.dropdown').hover(
        function() {
            $(this).find('.dropdown-menu').stop(true, true).delay(50).fadeIn();
        },
        function() {
            $(this).find('.dropdown-menu').stop(true, true).delay(50).fadeOut();
        }
    );
});



// Stores the number of days in the months of the year (January = 0...)
var month_length = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

/*  
    Fills in the mini-calendar specified table within the planner layout.

    @param year
        The year in XXXX format (i.e. 2015)
    @param month
        The month of the year (January = 0, December = 11)
    @param day
        The day of the week (Monday = 0, Sunday = 6)
*/
function miniCal(year, month, day) {
    var now = new Date();

    // Initialize our time variable with the input if it's valid.
    this.day = (isNaN(day) || day == null) ? now.getDate() : day;
    this.month = (isNaN(month) || month == null) ? now.getMonth() : month;
    this.year = (isNaN(year) || year == null) ? now.getFullYear() : year;
    this.html = "";

    this.getHTML = function() {
        return this.html;
    }

    // Creates the html of the calendar.
    this.generateHTML = function() {
        var monthLength = month_length[this.month];

        // Quick check to compensate for leap years
        if (this.month == 1) {
            if ((this.year % 4 == 0 && this.year % 100 != 0) || this.year % 400 == 0) {
                monthLength = 29;
            }
        }

        var firstDay = new Date(this.year, this.month, 1), 
            lastDay = new Date(this.year, this.month, monthLength),
            currentDay = new Date(this.year, this.month, this.day),
            firstDayInt = firstDay.getDay(),
            currentDayInt = currentDay.getDay(),
            lastDayInt = lastDay.getDay();

        // Variable to store the html that we'll write to the document
        var html = '<table class="planner-mini-calendar">' +
                        '<!--  7 equally spaced columns  -->' +
                        '<col><col><col><col><col><col><col>';
        /*
            Strategy: We know the first day, the month length and where the first day is in the week.

            So, first, populate the boxes to the left of the first day (if any).
            Populate the boxes of the month, and highlight the current week.

            Lastly, populate the boxes to the right of the last day (if any).
        */

        // Store how many days to the left of day 1, and the last number we need from those.
        var prevDays = firstDayInt == 0 ? 7 : firstDayInt,
            postDays = lastDayInt == 6 ? 7: 6 - lastDayInt;

        // Track where we are in the month
        var currentDay = 1;

        // Track where we need to start in the previous month
        var preMonth = this.month == 0 ? 12 : this.month - 1,
            preCurrentDay = month_length[preMonth] - prevDays + 1;

        // Loop for 6 weeks always (max number needed for the longest month)
        for(var calWeek = 0; calWeek < 6; calWeek++) {
            // If we're in the current week, highlight it.
            if( this.day - currentDayInt == currentDay 
                || (calWeek == 0 && this.day - currentDayInt < 1)) {
                html += '<tr class="planner-mini-calendar-active">';
            }
            else {
                html += '<tr>';
            }

            // Loop for 7 days (7 days per week)
            for(var calDay = 0; calDay < 7; calDay++) {
                // Previous month filler days
                if(calWeek == 0 && prevDays > 0) {
                    // Append the correct styles to these inactive cells
                    html += '<td class="planner-mini-calendar-inactive';

                    // If we're at the last child, use a custom style to fix bordering issues
                    if(prevDays == 1) {
                        html += '-last';
                    }
                    html += '">' + preCurrentDay + '</td>';
                    preCurrentDay++;
                    prevDays--;
                }
                // Post month filler days
                else if(postDays > 0 && currentDay > monthLength) {
                    html += '<td class="planner-mini-calendar-inactive">' + (currentDay - monthLength) + '</td>';
                    currentDay++;
                }
                // current month filler days
                else {
                    html += '<td>' + currentDay + '</td>';
                    currentDay++;
                }
            }
            html += '</tr>';
        }
        html += '</table>';
        this.html = html;
    }

    // Updates the calendar to the current date objects. 
    // #TODO connect this with the "current time" user attribute.
    this.handleDateChange = function() {
        
    }
} 