
$(function(){
  
  let $allPanels = $('.nested').hide();
  let $elements = $('.treeview-animated-element');

  $('.treeview-animated-items-header').click(function () {
      $this = $(this);
      $target = $this.siblings('.nested');
      $pointerPlus = $this.children('.fa-plus-circle');
      $pointerMinus = $this.children('.fa-minus-circle');

      $pointerPlus.removeClass('fa-plus-circle');
      $pointerPlus.addClass('fa-minus-circle');
      $pointerMinus.removeClass('fa-minus-circle');
      $pointerMinus.addClass('fa-plus-circle');
      $this.toggleClass('open')
      if (!$target.hasClass('active')) {
        $target.addClass('active').slideDown();
      } else {
        $target.removeClass('active').slideUp();
      }

      return false;
  });
  $elements.click(function () {
      $this = $(this);

      if ($this.hasClass('opened')) {

        $elements.removeClass('opened');
      } else {

        $elements.removeClass('opened');
        $this.addClass('opened');
      }
    })
  
})
