class Tone:
    NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    def __init__(self, note):
        self.note = note
        
    def __str__(self):
        return self.note
        
    def __add__(self, other):
        if isinstance(other, Interval):
            index = (self.NOTES.index(self.note) + other.semitones) % 12
            return Tone(self.NOTES[index])
        elif isinstance(other, Tone):
            return Chord(self, other)
        
    def __sub__(self, other):
        if isinstance(other, Tone):
            start = self.NOTES.index(other.note)
            end = self.NOTES.index(self.note)
            semitones = (end - start) % 12
            return Interval(semitones)
        elif isinstance(other, Interval):
            index = (self.NOTES.index(self.note) - other.semitones) % 12
            return Tone(self.NOTES[index])
        raise TypeError("Invalid operation")
        
    def __eq__(self, other):
        return isinstance(other, Tone) and self.note == other.note
        
    def __hash__(self):
        return hash(self.note)

class Interval:
    NAMES = {
        0: "perfect unison",
        1: "minor 2nd", 
        2: "major 2nd",
        3: "minor 3rd",
        4: "major 3rd",
        5: "perfect 4th",
        6: "tritone",
        7: "perfect 5th",
        8: "minor 6th",
        9: "major 6th", 
        10: "minor 7th",
        11: "major 7th"
    }
    
    def __init__(self, semitones):
        self.semitones = semitones % 12
        
    def __str__(self):
        return self.NAMES[self.semitones]
        
    def __add__(self, other):
        return Interval(self.semitones + other.semitones)
        
    def __neg__(self):
        return Interval(-self.semitones)

class Chord:
    def __init__(self, root, *notes):
        unique_notes = {root}
        for note in notes:
            unique_notes.add(note)
            
        if len(unique_notes) < 2:
            raise TypeError("Cannot have a chord made of only 1 unique tone")
            
        self.root = root
        self.notes = unique_notes
            
    def __str__(self):
        sorted_notes = sorted(self.notes, 
                            key=lambda x: (Tone.NOTES.index(x.note) - Tone.NOTES.index(self.root.note)) % 12)
        return "-".join(str(note) for note in sorted_notes)
        
    def is_minor(self):
        for note in self.notes:
            if (note - self.root).semitones == 3:
                return True
        return False
        
    def is_major(self):
        for note in self.notes:
            if (note - self.root).semitones == 4:
                return True
        return False
        
    def is_power_chord(self):
        return not (self.is_minor() or self.is_major())
        
    def __add__(self, other):
        if isinstance(other, Tone):
            return Chord(self.root, *(self.notes | {other}))
        elif isinstance(other, Chord):
            return Chord(self.root, *(self.notes | other.notes))
            
    def __sub__(self, other):
        if other not in self.notes:
            raise TypeError(f"Cannot remove tone {other} from chord {self}")
            
        remaining = self.notes - {other}
        if len(remaining) < 2:
            raise TypeError("Cannot have a chord made of only 1 unique tone")
            
        return Chord(self.root, *(note for note in remaining if note != self.root))
        
    def transposed(self, interval):
        if isinstance(interval, int):
            interval = Interval(interval)
        return Chord(self.root + interval, 
                    *(note + interval for note in self.notes if note != self.root))
