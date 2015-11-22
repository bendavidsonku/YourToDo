$(document).ready(function() {
    $('.btn-layout-selector').click(function() {
        if(localStorage.layoutType = $(this).html()) {
            // Do nothing
        }
        else {
            localStorage.layoutType = $(this).html();
            changeViewLayout();
        }
    });

    // Prevent highlighting when clicking date selectors too fast
    $('.planner-date-selectors-button').mousedown(function(e) {
        e.preventDefault();
    });


    // Session Storage
    if (!(sessionStorage.viewDate)) {
        var now = new Date();
        sessionStorage.viewDate = now;
    }

    // Local Storage
    if (!(localStorage.layoutType)) {
        localStorage.layoutType = "Week";
    }

    changeViewDate("FIRST", 0);
    changeViewLayout();
});

/*
    Renders the current layoutType to the page

    #TODO Actually make this work with different layouts
*/
function changeViewLayout() {
    var btns = $(".btn-layout-selector");

    // Remove active from all buttons
    for(var index = 0; index < btns.length; index++) {
         $(btns[index]).removeClass('active');
    }

    // 'Activate' the button that was clicked
    switch(localStorage.layoutType) {
    case 'Day':
        $('#btn-layout-day').addClass('active');
        break;
    case 'Week':
        $('#btn-layout-week').addClass('active');
        break;
    case 'Month':
        $('#btn-layout-month').addClass('active');
        break;
    default:
        console.log("Invalid layoutType: " + localStorage.layoutType);
        break;

    // #TODO --> Link to different view or something.
    }
}


// Returns the current viewDate stored in sessionStorage
function getViewDate() {
    return new Date(Date.parse(sessionStorage.viewDate));
}

/*
    Changes the current viewDate in sessionStorage based on input:

    @param size
        The size of the change: DAY, WEEK, MONTH, YEAR
    @param amount
        The amount of the change: -1, or 1, preferrably. (1 week, 1 month, -1 week, etc.)

    Prompts all date fields to update to the new viewDate
    Prompts the mini calendar to re-write itself if it's displayed.
*/
function changeViewDate(size, amount) {
    var viewDate = getViewDate();

    if(size === "DAY") {
        viewDate.setDate(viewDate.getDate() + amount);
    }
    else if(size === "WEEK") {
        viewDate.setDate(viewDate.getDate() + 7 * amount);
    }
    else if(size === "MONTH") {
        viewDate.setMonth(viewDate.getMonth() + amount);
    }
    else if(size === "YEAR") {
        viewDate.setFullYear(viewDate.getFullYear() + amount);
    }
    else if(size === "FIRST") {
        // Do nothing, just running first time set up.
    }
    else {
        console.log("changeViewDate() unknown parameter: " + size);
    }

    sessionStorage.viewDate = viewDate;
    var start_date = getDateOfDay(0),
        end_date   = getDateOfDay(6);

    // Update events based on the new view
    $.ajax({
        url: "/load-events/",
        type: "POST",
        dataType: 'html',
        data: 
        {
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
            view_start_date: start_date,
            view_end_date: end_date
        },
        success: function(data, textStatus, jqXHR) {
            $('#events-in-categories').html(data);
            console.log(data);
        },
    });

    // Update all fields in case they changed
    document.getElementById("planner-date-month-selector").innerHTML = month_names[viewDate.getMonth()];
    document.getElementById("planner-date-week-selector").innerHTML = getWeekString();
    document.getElementById("planner-date-year-selector").innerHTML = viewDate.getFullYear();

    // If the mini calendar is on the page (day & week views), update it
    // Don't update it if this is the first time running this function
    if(localStorage.layoutType != "Month" && size != "FIRST") {
        this.miniCal.handleDateChange();
    }
}

// Store the month lengths & names
var month_length = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
    month_names = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'June', 'July',
                   'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.'],
    month_names_long = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                   'August', 'September', 'October', 'November', 'December'];

// Do not ask me to explain this function because I don't want to spend an hour re-learning it.
this.getWeekString = function() {
    var viewDate = getViewDate(),
        month = viewDate.getMonth() + 1;
        // Start weekSunday at the current day - today's week index
        weekSunday = viewDate.getDate() - viewDate.getDay(),
        // Logically, weekSaturday is 6 days away from weekSunday
        weekSaturday = weekSunday + 6,
        // Assume the same month
        monthNum1 = monthNum2 = month;
        
    // If weekSunday is negative, it goes into the previous month
    if(weekSunday <= 0) {
        monthNum1 = month == 1 ? 12 : month - 1;
        // weekSunday still holds the overflow, so use it to get the sunday date from previous month
        weekSunday = month_length[monthNum1 - 1] + weekSunday;
    }

    // If weekSaturday is > the month length of this month, it extends into following month
    if(weekSaturday > month_length[month - 1]) {
        weekSaturday -= month_length[month - 1];
        monthNum2 = month == 12 ? 1 : month + 1;
    }

    // Return a string in the followin format: "7/1 - 7/7"
    return monthNum1 + "/" + weekSunday + " - " + monthNum2 + "/" + weekSaturday;
}

/*  
    Fills in the mini-calendar specified table within the planner layout.

    @param year
        The year in XXXX format (i.e. 2015)
    @param month
        The month of the year (January = 0, December = 11)
    @param day
        The day of the week (Monday = 0, Sunday = 6)

    @note
        Use no parameters to use the current viewDate stored in sessionStorage

    #TODO --> Be able to click on days and then update the cal/viewDate to that day.
*/
this.miniCal = function(year, month, day) {
    viewDate = getViewDate();

    // Initialize our time variable with the input if it's valid.
    this.day = (isNaN(day) || day == null) ? viewDate.getDate() : day;
    this.month = (isNaN(month) || month == null) ? viewDate.getMonth() : month;
    this.year = (isNaN(year) || year == null) ? viewDate.getFullYear() : year;
    this.html = "";

    // Returns the html (assuming it has been previously generated)
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
            currentDay = 1; // Use this to track where we are in the month
            lastDayInt = lastDay.getDay();

        // Variable to store the html that we'll write to the document
        var html = '<table class="planner-mini-calendar">' +
                        '<!--  7 equally spaced columns  -->' +
                        '<col><col><col><col><col><col><col>';

        // Store how many days to the left of day 1, and the last number we need from those.
        var prevDays = firstDayInt == 0 ? 7 : firstDayInt,
            postDays = lastDayInt == 6 ? 7: 6 - lastDayInt;

        // Find the integer value of the day in the previous month we need to start counting at
        var preCurrentDay = month_length[this.month == 0 ? 11 : this.month - 1] - prevDays + 1;
        
        // Loop for 6 weeks always (max number needed for the longest month)
        for(var calWeek = 0; calWeek < 6; calWeek++) {
            // If we're in the current week, highlight it.
            if((this.day - currentDayInt == currentDay && prevDays != 7) ||
               (calWeek == 0 && this.day - currentDayInt < 1)) {
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
                // If we're not filling pre or post days, that means we're still filling current month days
                else {
                    html += '<td>' + currentDay + '</td>';
                    currentDay++;
                }
            }
            html += '</tr>';
        }
        html += '</table>';

        // Store the generated html in our variable defined at class level
        this.html = html;
    }

    // Updates the calendar to the current view date
    this.handleDateChange = function() {
        viewDate = getViewDate();

        this.day = viewDate.getDate();
        this.month = viewDate.getMonth();
        this.year = viewDate.getFullYear();

        this.generateHTML();
        document.getElementById("planner-mini-calendar").innerHTML = this.getHTML();
    }
} 

// Returns the date of the specified day in the week
getDateOfDay = function(day) {
    date = getViewDate();
    date.setDate(date.getDate() - date.getDay() + day);

    monthPadding = "";

    if(date.getMonth() + 1 <= 9) {
        monthPadding = "0";
    }

    // Return the date string ("2015-11-21" for example)
    return date.getFullYear() + "-" + monthPadding + (date.getMonth() + 1) + "-" + date.getDate();
}