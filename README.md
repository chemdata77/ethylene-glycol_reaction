# ethylene-glycol_reaction

1.generate_reaction_gibbs.py (qm9-->Reactant_reactions_gibbs.txt/out_reactions_gibbs.txt)
2.generate_reaction_homolumo.py (qm9-->Reactant_reactions_homolumo.txt/out_reactions_homolumo.txt)
3.read_reac_g.py (Reactant_reactions_gibbs.txt-->Reactant_reactions_g_yes.txt and Reactant_reactions_g_no.txt)
4.read_reac_hl.py (Reactant_reactions_homolumo.txt-->Reactant_reactions_hl_yes.txt and Reactant_reactions_hl_no.txt)
5.Reactant_read_rec_all.py (Reactant_reactions_gibbs.txt and Reactant_reactions_homolumo.txt-->Reactant_reactions_all.txt)
6.out_read_rec_all.py (out_reactions_gibbs.txt and out_reactions_homolumo.txt-->out_reactions_all.txt)
7.draw.py (Reactant_reactions_all.txt and qm9.csv-->picture, out_reactions_all.txt-->picture_out)
8.reac_word.py (Reactant_reactions_all.txt and picture-->Reactant_reactions.doc, out_reactions_all.txt and picture_out-->out_reactions.docx )
