from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import PokemonCard, Binder
from .utils import search_card
import math

# Create your views here.
def index(request):
    return render(request, "collection/index.html")

def binder_shelf(request):
    binders = Binder.objects.order_by('created_at')
    return render(request, "collection/binder_shelf.html", {'binders': binders, 'capacity': 180})

@require_http_methods(["POST"])
def create_binder(request):
    if Binder.objects.count() >= 3:
        return redirect('binder_shelf')
        
    name = request.POST.get('name')
    description = request.POST.get('description', '')
    if name:
        binder = Binder.objects.create(name=name, description=description)
        # Redirect to the cover of the new binder (Page 1)
        return redirect('binder_page', binder_id=binder.id, page=1)
    return redirect('binder_shelf')

def search_cards(request):
    query = request.GET.get('q', '')
    binder_id = request.GET.get('binder_id')
    page_num = request.GET.get('page', 1)
    position = request.GET.get('position')
    cards = search_card(query)
    return render(request, 'collection/partials/search_results.html', {
        'cards': cards, 'binder_id': binder_id, 'page': page_num, 'position': position
    })

@require_http_methods(["POST"])
def add_card(request, binder_id):
    binder = get_object_or_404(Binder, pk=binder_id)
    
    # Get card data from form (we'll implement this form in the result item)
    name = request.POST.get('name')
    card_id = request.POST.get('card_id')
    image_url = request.POST.get('image_url')
    set_name = request.POST.get('set_name')
    
    target_page = int(request.POST.get('page', 1))
    explicit_position = request.POST.get('position')
    
    if explicit_position and explicit_position != 'None' and explicit_position != '':
        position = int(explicit_position)
        # We trust the user wants it here. If there's already a card, they will overlap (acceptable for now)
        # or we could shift things. For this request, "place directly in the box" implies exact position.
    else:
        # Calculate start position for this page
        if target_page == 1:
            start_pos = 1
        else:
            start_pos = 10 + (target_page - 2) * 18

        # Find the first available position starting from this page
        used_positions = set(PokemonCard.objects.filter(binder=binder).values_list('position', flat=True))
        position = start_pos
        while position in used_positions:
            position += 1

    # Create card and assign to this binder
    PokemonCard.objects.create(
        binder=binder,
        name=name,
        card_id=card_id,
        image_url=image_url,
        set_name=set_name,
        position=position
    )
    
    # Return to the binder view (or trigger a refresh)
    # Redirect to the page we just added to (which is likely target_page, unless it overflowed)
    return redirect('binder_page', binder_id=binder.id, page=target_page)
    # For now, just go to the open binder (Page 1)
    return redirect('binder_page', binder_id=binder.id, page=1)

def binder(request, binder_id, page=1):
    current_binder = get_object_or_404(Binder, pk=binder_id)

    # Check if this is a request for the Search Modal
    if request.htmx and request.GET.get('modal') == 'true':
         page_num = request.GET.get('page', 1)
         position = request.GET.get('position')
         return render(request, 'collection/partials/search_modal.html', {
             'binder': current_binder, 
             'page': page_num,
             'position': position
         })

    # Fetch Real Cards for this Binder
    all_cards = list(PokemonCard.objects.filter(binder=current_binder))
    
    # Pagination Logic
    # Page 0: Cover (No cards)
    # Page 1: 9 cards (Right side only)
    # Page 2+: 18 cards (Left and Right sides)
    
    if page == 0:
        # Cover View
        context = {
            'binder': current_binder,
            'page': 0,
            'is_cover': True,
            'is_first_page': False,
            'slots': [],
            'total_pages': 0, # Placeholder
            'has_next': True,
            'has_previous': False,
            'next_page': 1,
            'previous_page': None,
        }
        # Calculate Total Pages for context (same formula)
        total_cards = len(all_cards)
        if total_cards <= 9:
            context['total_pages'] = 1
        else:
            remaining = total_cards - 9
            context['total_pages'] = 1 + math.ceil(remaining / 18)
            
        return render(request, "collection/binder.html", context)

    if page == 1:
        start_pos = 1
        end_pos = 9
        slots_needed = 9
    else:
        # Page 1 took positions 1-9.
        # Page 2 starts at 10, ends at 10 + 17 = 27 (Wait, logic check)
        # Old logic: Page 2 starts after 9 items.
        # New logic: Page 2 is positions 10 to 27 (18 items).
        start_pos = 10 + (page - 2) * 18
        end_pos = start_pos + 17 # Inclusive range
        slots_needed = 18
        
    # Get the cards for this page range
    page_cards = PokemonCard.objects.filter(
        binder=current_binder, 
        position__gte=start_pos, 
        position__lte=end_pos
    )
    
    # Create a map of position -> card
    card_map = {card.position: card for card in page_cards}
    
    # Build the slots list
    current_slots = []
    for i in range(slots_needed):
        current_pos = start_pos + i
        current_slots.append({
            'card': card_map.get(current_pos),
            'position': current_pos
        })
        
    # Calculate Total Pages based on the highest position card
    # This might leave empty pages if there's a huge gap, but it's consistent.
    # Alternatively, count total items and do math? 
    # Let's stick to total items logic for now, but really "last page" is determined by max position.
    # Fixed Binder Capacity Logic
    # 180 Cards Total
    # Page 1: 9 Cards
    # Remaining: 171 Cards -> ceil(171 / 18) = 10 pages
    # Total Pages: 1 + 10 = 11
    
    total_pages = 11
    
    # Optional: If we want to support multiple binder sizes later, we can add a 'capacity' field to Binder model.
    # For now, hardcoded to 11 pages (180 cards).

    context = {
        'binder': current_binder,
        'page': page,
        'slots': current_slots,
        'is_cover': False,
        'is_first_page': (page == 1),
        'total_pages': total_pages,
        'has_next': page < total_pages,
        'has_previous': True, # Page 1 can go back to 0
        'next_page': page + 1,
        'previous_page': page - 1 if page > 1 else 0,
    }
    
    return render(request, "collection/binder.html", context)

@require_http_methods(["POST"])
def delete_binder(request, binder_id):
    binder = get_object_or_404(Binder, pk=binder_id)
    binder.delete()
    return redirect('binder_shelf')

@require_http_methods(["POST"])
def delete_card(request, card_id):
    card = get_object_or_404(PokemonCard, pk=card_id)
    binder_id = card.binder.id
    # Calculate which page the card was on to redirect back to the same page
    # This is a bit complex because cards shift. 
    # For now, let's just redirect to page 1 or the binder cover.
    # Refined UX: Redirect to the page the card *was* on? 
    # Since we don't track page in card model, we'd need to calculate it on the fly or pass it in.
    # Passing it in via query param or form data is best.
    
    page = request.POST.get('page', 1)
    
    card.delete()
    return redirect('binder_page', binder_id=binder_id, page=page)

