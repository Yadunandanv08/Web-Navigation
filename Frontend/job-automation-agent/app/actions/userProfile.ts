'use server';

import { auth, db } from '@/lib/firebase';
import { doc, getDoc, setDoc, updateDoc, serverTimestamp } from 'firebase/firestore';

interface UserProfile {
  uid: string;
  email: string;
  displayName?: string;
  photoURL?: string;
  resumeURL?: string;
  jobTitle?: string;
  about?: string;
  createdAt?: any;
  updatedAt?: any;
}

export async function getUserProfile(uid: string): Promise<UserProfile | null> {
  try {
    const userDocRef = doc(db, 'users', uid);
    const userDocSnap = await getDoc(userDocRef);
    
    if (userDocSnap.exists()) {
      return userDocSnap.data() as UserProfile;
    }
    return null;
  } catch (error) {
    console.error('[getUserProfile] Error:', error);
    throw new Error('Failed to fetch user profile');
  }
}

export async function initializeUserProfile(
  uid: string,
  email: string,
  displayName?: string,
  photoURL?: string
): Promise<UserProfile> {
  try {
    const userDocRef = doc(db, 'users', uid);
    const userDocSnap = await getDoc(userDocRef);
    
    if (!userDocSnap.exists()) {
      const newProfile: UserProfile = {
        uid,
        email,
        displayName: displayName || '',
        photoURL: photoURL || '',
        createdAt: serverTimestamp(),
        updatedAt: serverTimestamp(),
      };
      
      await setDoc(userDocRef, newProfile);
      return newProfile;
    }
    
    return userDocSnap.data() as UserProfile;
  } catch (error) {
    console.error('[initializeUserProfile] Error:', error);
    throw new Error('Failed to initialize user profile');
  }
}

export async function updateUserProfile(
  uid: string,
  updates: Partial<UserProfile>
): Promise<UserProfile> {
  try {
    const userDocRef = doc(db, 'users', uid);
    const updateData = {
      ...updates,
      updatedAt: serverTimestamp(),
    };
    
    await updateDoc(userDocRef, updateData);
    
    const updatedDocSnap = await getDoc(userDocRef);
    return updatedDocSnap.data() as UserProfile;
  } catch (error) {
    console.error('[updateUserProfile] Error:', error);
    throw new Error('Failed to update user profile');
  }
}
