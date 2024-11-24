import React from 'react';
import './Seasonal.css'

// Helper function to check if a date is the 4th Thursday of November (Thanksgiving)
const isThanksgiving = (date) => {
  const year = date.getFullYear();
  const thanksgiving = new Date(year, 10, 1); // November 1st
  const dayOfWeek = thanksgiving.getDay(); // Get the day of the week for November 1st
  const offset = (4 - dayOfWeek + 7) % 7; // Get the offset to the first Thursday
  thanksgiving.setDate(1 + offset + 21); // Set the date to the 4th Thursday
  return thanksgiving;
};

// Helper function to check if the date is Memorial Day (last Monday of May)
const isMemorialDay = (date) => {
  const year = date.getFullYear();
  const memorialDay = new Date(year, 4, 31); // May 31st
  memorialDay.setDate(memorialDay.getDate() - memorialDay.getDay()); // Move to the last Monday
  return memorialDay;
};

// Helper function to check if it's Labor Day (first Monday of September)
const isLaborDay = (date) => {
  const year = date.getFullYear();
  const laborDay = new Date(year, 8, 1); // September 1st
  const dayOfWeek = laborDay.getDay();
  const offset = (1 - dayOfWeek + 7) % 7; // Get the offset to the first Monday
  laborDay.setDate(1 + offset); // Set the date to the first Monday
  return laborDay;
};

// Helper function to check if the date is New Year's Day (January 1)
const isNewYearsDay = (date) => {
  const year = date.getFullYear();
  return new Date(year, 0, 1); // January 1st
};

// Helper function to check if the date is Independence Day (July 4)
const isIndependenceDay = (date) => {
  const year = date.getFullYear();
  return new Date(year, 6, 4); // July 4th
};

// Helper function to check if the date is Christmas (December 25)
const isChristmas = (date) => {
  const year = date.getFullYear();
  return new Date(year, 11, 25); // December 25th
};

// Helper function to calculate the range 10 days before the holiday
const isWithinHolidayRange = (holidayDate, currentDate) => {
  const startDate = new Date(holidayDate);
  startDate.setDate(holidayDate.getDate() - 10); // 10 days before the holiday
  
  const endDate = new Date(holidayDate); // The day of the holiday
  
  // Check if the current date is within the range of start and end dates
  return currentDate >= startDate && currentDate <= endDate;
};

const Seasonal = () => {
  const currentDate = new Date();
  
  // Get the specific holiday dates
  const newYearsDay = isNewYearsDay(currentDate);
  const independenceDay = isIndependenceDay(currentDate);
  const thanksgivingDay = isThanksgiving(currentDate);
  const laborDay = isLaborDay(currentDate);
  const memorialDay = isMemorialDay(currentDate);
  const christmasDay = isChristmas(currentDate);
  
  // Holiday theme settings
  let holidayTheme = '';
  let holidayMessage = '';
  let holidayGreeting = '';

  // Set holiday theme based on current holiday
  if (isWithinHolidayRange(newYearsDay, currentDate)) {
    holidayTheme = 'new-years-theme';
    holidayMessage = 'Happy New Year!';
    holidayGreeting = 'Ring in the New Year with the best movies!';
  } else if (isWithinHolidayRange(independenceDay, currentDate)) {
    holidayTheme = 'independence-day-theme';
    holidayMessage = 'Happy Independence Day!';
    holidayGreeting = 'Celebrate with action-packed movies!';
  } else if (isWithinHolidayRange(thanksgivingDay, currentDate)) {
    holidayTheme = 'thanksgiving-theme';
    holidayMessage = 'Happy Thanksgiving!';
    holidayGreeting = 'Time for a fun movie feast!';
  } else if (isWithinHolidayRange(christmasDay, currentDate)) {
    holidayTheme = 'christmas-theme';
    holidayMessage = 'Merry Christmas!';
    holidayGreeting = 'Enjoy the best Christmas movies!';
  } else if (isWithinHolidayRange(laborDay, currentDate)) {
    holidayTheme = 'labor-day-theme';
    holidayMessage = 'Happy Labor Day!';
    holidayGreeting = 'Relax with a movie on Labor Day!';
  } else if (isWithinHolidayRange(memorialDay, currentDate)) {
    holidayTheme = 'memorial-day-theme';
    holidayMessage = 'Happy Memorial Day!';
    holidayGreeting = 'Honor the day with great movies!';
  }

  return (
    <div className={`container holiday-page ${holidayTheme}`}>
      <div className="holiday-header text-center">
        <h1>{holidayMessage}</h1>
        <p>{holidayGreeting}</p>
      </div>
      
      <div className="holiday-buttons text-center">
        {/* New Year's Day Button */}
        {isWithinHolidayRange(newYearsDay, currentDate) && (
          <button className="btn btn-primary" onClick={() => window.open("https://www.imdb.com/list/ls522631204/", "_blank")}>
            Get the Best New Year's Movies
          </button>
        )}

        {/* Independence Day Button */}
        {isWithinHolidayRange(independenceDay, currentDate) && (
          <button className="btn btn-danger" onClick={() => window.open("https://www.imdb.com/list/ls528659350/", "_blank")}>
            Get the Best Independence Day Movies
          </button>
        )}

        {/* Thanksgiving Button */}
        {isWithinHolidayRange(thanksgivingDay, currentDate) && (
          <button className="btn btn-warning" onClick={() => window.open("https://www.imdb.com/list/ls000835734/", "_blank")}>
            Get the Best Thanksgiving Movies
          </button>
        )}

        {/* Christmas Button */}
        {isWithinHolidayRange(christmasDay, currentDate) && (
          <button className="btn btn-success" onClick={() => window.open("https://www.imdb.com/list/ls000096828/", "_blank")}>
            Get the Best Christmas Movies
          </button>
        )}

        {/* Labor Day Button */}
        {isWithinHolidayRange(laborDay, currentDate) && (
          <button className="btn btn-info" onClick={() => window.open("https://www.imdb.com/list/ls002014923/", "_blank")}>
            Get the Best Labor Day Movies
          </button>
        )}

        {/* Memorial Day Button */}
        {isWithinHolidayRange(memorialDay, currentDate) && (
          <button className="btn btn-dark" onClick={() => window.open("https://www.imdb.com/list/ls561621160/", "_blank")}>
            Get the Best Memorial Day Movies
          </button>
        )}
      </div>
    </div>
  );
};

export default Seasonal;