from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Animal, Equipement
import copy


def animal_list(request):
    animals = Animal.objects.filter()
    return render(request, 'animalerie/animal_list.html', {'animals': animals})


def equipement_list(request):
    equipements = Equipement.objects.filter()
    return render(request, 'animalerie/equipement_list.html', {'equipements': equipements})


# def animal_detail(request, id_animal):
#     animal = get_object_or_404(Animal, id_animal=id_animal)
#     lieu = get_object_or_404(Equipement, id_equip=animal.lieu)
#     message = ''
#     ancien_lieu = copy.deepcopy(lieu)
#     if request.method == "POST":
#         form = MoveForm(request.POST, instance=animal)
#     else:
#         form = MoveForm()
#     if form.is_valid():
#         form.save(commit=False)
#         nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
#         if animal.lieu.disponibilite == "Occupé" and nouveau_lieu != "Litière":
#             message = "Le lieu est Occupé, impossible de s'y déplacer."
#             return redirect('animal_detail', id_animal=id_animal)
#         else:
#             ancien_lieu.disponibilite = "Libre"
#             ancien_lieu.save()
#             form.save()
#             nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
#             if nouveau_lieu != "Litière":
#                 nouveau_lieu.disponibilite = "Occupé"
#             nouveau_lieu.save()
#             return redirect('animal_detail', id_animal=id_animal)
#     else:
#         form = MoveForm()
#         return render(request,
#                       'animalerie/animal_detail.html',
#                       {'animal': animal, 'lieu': lieu, 'form': form})


def animal_detail(request, id_animal):
    animal = get_object_or_404(Animal, id_animal=id_animal)
    lieu = get_object_or_404(Equipement, id_equip=animal.lieu)
    message = ''
    ancien_lieu = copy.deepcopy(lieu)
    if request.method == "POST":
        form = MoveForm(request.POST, instance=animal)
    else:
        form = MoveForm()
    if form.is_valid():
        form.save(commit=False)
        if animal.lieu.disponibilite == 'Libre':
            if animal.etat == 'Fatigué' and animal.lieu.id_equip == 'Nid':
                animal.etat = 'Endormi'
                animal.save()
                ancien_lieu.disponibilite = "Libre"
                ancien_lieu.save()
                nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
                nouveau_lieu.disponibilite = "Occupé"
                nouveau_lieu.save()
                return redirect('animal_detail', id_animal=id_animal)
            if animal.etat == 'Affamé' and animal.lieu.id_equip == 'mangeoire':
                animal.etat = 'Repus'
                animal.save()
                ancien_lieu.disponibilite = "Libre"
                ancien_lieu.save()
                nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
                nouveau_lieu.disponibilite = "Occupé"
                nouveau_lieu.save()
                return redirect('animal_detail', id_animal=id_animal)
            if animal.etat == 'Repus' and animal.lieu.id_equip=='Roue' :
                animal.etat = 'Fatigué'
                animal.save()
                ancien_lieu.disponibilite = "Libre"
                ancien_lieu.save()
                nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
                nouveau_lieu.disponibilite = "Occupé"
                nouveau_lieu.save()
                return redirect('animal_detail', id_animal=id_animal)
            if animal.etat == 'Endormi' and animal.lieu.id_equip == 'Litière':
                animal.etat = 'Affamé'
                animal.save()
                ancien_lieu.disponibilite = "Libre"
                ancien_lieu.save()
                nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
                nouveau_lieu.disponibilite = "Libre"
                nouveau_lieu.save()
                return redirect('animal_detail', id_animal=id_animal)
            else:
                message = "L'état de l'animal n'est pas adapté à cette activité."
                return render(request,
                              'animalerie/animal_detail.html',
                              {'animal': animal, 'lieu': lieu, 'form': form, 'message': message})
        else:
            message = "Lieu déjà occupé"
            return render(request,
                          'animalerie/animal_detail.html',
                          {'animal': animal, 'lieu': lieu, 'form': form, 'message': message})
    else:
        form = MoveForm()
        return render(request,
                      'animalerie/animal_detail.html',
                      {'animal': animal, 'lieu': lieu, 'form': form, 'message': message})
