// cancel_reservation
function cancelReservation(reservationId) {
    // Perform an AJAX request to cancel the reservation
    $.ajax({
      url: "/cancel_reservation",
      method: "POST",
      data: { reservationId: reservationId },
      success: function(response) {
        // Handle the success response
        console.log("Reservation cancelled successfully");
        // Optionally, you can update the UI to reflect the canceled reservation
      },
      error: function(error) {
        // Handle the error response
        console.error("Error cancelling reservation", error);
      }
    });
  }
  