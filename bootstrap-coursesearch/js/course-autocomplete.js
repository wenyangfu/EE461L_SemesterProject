$(function(){
  var courses = [
    { value: 'EE302 Introduction to Electrical Engineering', data: 'EE302' },
    { value: 'EE306 Introduction to Computing', data: 'EE306' },
    { value: 'EE309S Devel of Solar-Powered Vehicle', data: 'EE309S' },
    { value: 'EE411 Circuit Theory', data: 'EE411' },
    { value: 'EE312 Software Design and Implementation 1', data: 'EE312' },
    { value: 'EE313 Linear Systems and Signals', data: 'EE313' },
    { value: 'EE316 Digital Logic Design', data: 'EE316' },
    { value: 'EE319K Introduction to Embedded Systems', data: 'EE319K' },
    { value: 'EE422C Software Design and Implementation 2', data: 'EE422C' },
    { value: 'EE325 Electromagnetic Engineering', data: 'EE325' },
    { value: 'EE325K Antennas and Wireless Propagation', data: 'EE325K' },
    { value: 'EE325LX Cooperative Engineering', data: 'EE325LX' },
    { value: 'EE325LY Cooperative Engineering', data: 'EE325LY' },
    { value: 'EE325LZ Cooperative Engineering', data: 'EE325LZ' },
    { value: 'EE225MA Cooperative Engineering', data: 'EE225MA' },
    { value: 'EE225MB Cooperative Engineering', data: 'EE225MB' },
    { value: 'EE125N Cooperative Engineering', data: 'EE125N' },
    { value: 'EE125S Internship in Electrical and Computer Engineering', data: 'EE125S' },
    { value: 'EE333T Engineering Communication', data: 'EE333T' },
    { value: 'EE438 Fundamentals of Electrical Circuits 1 Lab', data: 'EE438' },
    { value: 'EE338L Analog Integrated Circuit Design', data: 'EE338L' },
    { value: 'EE339 Solid-State Elecronic Devices', data: 'EE339' },
    { value: 'EE440 Integrated Circuit Nanomanufacturing Techniques', data: 'EE440' },
    { value: 'EE445L Embedded Systems Design Lab', data: 'EE445L' },
    { value: 'EE445S Real-Time Digital Signal Processing Lab', data: 'EE445S' },
    { value: 'EE351K Probability and Random Processes', data: 'EE351K' },
    { value: 'EE351M Digital Signal Processing', data: 'EE351M' },
    { value: 'EE160 Special Problems in Electrical and Computer Engineering', data: 'EE160' },
    { value: 'EE260 Special Problems in Electrical and Computer Engineering', data: 'EE260' },
    { value: 'EE360 Special Problems in Electrical and Computer Engineering', data: 'EE360' },
    { value: 'EE460 Special Problems in Electrical and Computer Engineering', data: 'EE460' },
    { value: 'EE360C Algorithms', data: 'EE360C' },
    { value: 'EE360F Introduction to Software Engineering', data: 'EE360F' },
    { value: 'EE460M Digital Systems Design Using HDL', data: 'EE460M' },
    { value: 'EE460N Computer Architecture', data: 'EE460N' },
    { value: 'EE460R Introduction to VLSI Design', data: 'EE460R' },
    { value: 'EE461L Software Engineering and Design Lab', data: 'EE461L' },
    { value: 'EE361Q Requirements Engineering', data: 'EE361Q' },
    { value: 'EE362K Introduction to Automatic Control', data: 'EE362K' },
    { value: 'EE462L Power Electronics Lab', data: 'EE462L' },
    { value: 'EE362S Development of Solar-Powered Vehicle', data: 'EE362S' },
    { value: 'EE363N Engineering Acoustics', data: 'EE363N' },
    { value: 'EE364D Introduction to Engineering Design', data: 'EE364D' },
    { value: 'EE364E Interdisciplinary Entrepreneurship', data: 'EE364E' },
    { value: 'EE464H Honors Senior Design Project', data: 'EE464H' },
    { value: 'EE464K Senior Design Project', data: 'EE464K' },
    { value: 'EE464R Research Senior Design Project', data: 'EE464R' },
    { value: 'EE369 Power Systems Engineering', data: 'EE369' },
    { value: 'EE371R Digital Image and Video Processing', data: 'EE71R' },
    { value: 'EE372N Telecommunication Networks', data: 'EE372N' },
    { value: 'EE374K Biomedical Electrical Instrument Design', data: 'EE374K' },
    { value: 'EE679HA Undergraduate Honors Thesis', data: 'EE679HA' },
    { value: 'EE379K Operating Systems', data: 'EE379K' },
  ];
  
  // setup autocomplete function pulling from currencies[] array
  $('#autocomplete').autocomplete({
    lookup: courses,
    onSelect: function (suggestion) {
      var thehtml = '<strong>Course Name:</strong> ' + suggestion.value + ' <br> <strong>Symbol:</strong> ' + suggestion.data;
      $('#outputcontent').html(thehtml);
    }
  });
  

});
